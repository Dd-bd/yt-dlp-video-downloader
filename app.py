import os
import re
import sys
import uuid
import time
import socket
import shutil
import logging
import threading
import subprocess

import psutil
import webview
from flask import Flask, render_template, request, jsonify

# ---------------------------------------------------------------------------
# 基础配置
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_ROOT = os.path.join(BASE_DIR, "downloads")
COOKIE_FILE = os.path.join(BASE_DIR, "cookies.txt")
LOG_FILE = os.path.join(BASE_DIR, "app.log")
os.makedirs(SAVE_ROOT, exist_ok=True)

# 打包成 windowed（console=False）后 sys.stdout/stderr 为 None，直接 print 会崩溃，
# 这里统一重定向到日志文件，既避免崩溃也便于排查。
if sys.stdout is None or sys.stderr is None:
    _log_stream = open(LOG_FILE, "a", encoding="utf-8")
    if sys.stdout is None:
        sys.stdout = _log_stream
    if sys.stderr is None:
        sys.stderr = _log_stream

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__)

# 远程组件开关：默认关闭，不从 GitHub 拉取并执行远程代码（避免供应链风险）。
# 个别依赖 EJS 解密的站点（如 Niconico）可能受影响，需要时改为 True。
REMOTE_EJS = False

# 最大并发下载数：由 worker_semaphore 真正执行限制（修复原“定义了但没用”的问题）。
MAX_WORKER = 3

# 接口鉴权 token：启动时随机生成并注入前端，防止本机其他进程/网页直接调用本地接口。
AUTH_TOKEN = uuid.uuid4().hex

# 进度模板：让 yt-dlp 每条进度独占一行，用 | 分隔；文件名放在最后一段（允许含 |）。
PROGRESS_TMPL = "PROGRESS|%(progress.status)s|%(progress._percent_str)s|%(progress.filename)s"
AUDIO_EXTS = {".m4a", ".m4b", ".mp3", ".opus", ".ogg", ".aac", ".flac", ".wav", ".aiff"}

# ---------------------------------------------------------------------------
# 全局状态
# ---------------------------------------------------------------------------
progress_store = {}
store_lock = threading.Lock()
proc_list = []
worker_semaphore = threading.Semaphore(MAX_WORKER)
task_queue = []
queue_lock = threading.Lock()
exit_event = threading.Event()


def find_free_port(start=5000, attempts=20):
    """找一个可用的本地端口，避免 5000 被占用时静默失败。"""
    for port in range(start, start + attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
            return port
        except OSError:
            continue
    raise RuntimeError(f"本地端口 {start}-{start + attempts - 1} 均被占用，无法启动")


def find_deno():
    """优先使用程序目录下的 deno.exe，其次查找 PATH。"""
    local = os.path.join(BASE_DIR, "deno.exe")
    if os.path.exists(local):
        return local
    return shutil.which("deno")


def find_ffmpeg():
    """优先使用程序目录下的 ffmpeg.exe，其次查找 PATH。"""
    local = os.path.join(BASE_DIR, "ffmpeg.exe")
    if os.path.exists(local):
        return local
    return shutil.which("ffmpeg")


def sanitize_filename(name):
    """去掉 Windows 文件名非法字符和路径分隔符，防止路径穿越。"""
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)
    name = name.strip().strip(".")
    return name or "video"


def build_output_template(save_name):
    """根据用户填写的保存名构建输出模板；留空则用视频标题。"""
    if save_name:
        return os.path.join(SAVE_ROOT, sanitize_filename(save_name) + ".%(ext)s")
    return os.path.join(SAVE_ROOT, "%(title)s [%(id)s].%(ext)s")


def kill_process_tree(pid):
    """递归结束进程及其所有子进程（yt-dlp 派生出的 ffmpeg、deno 等）。"""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
        parent.kill()
    except psutil.NoSuchProcess:
        pass


def queue_consumer():
    """消费队列：逐个取出任务并启动线程，真正的并发上限由信号量保证。"""
    while True:
        task_item = None
        with queue_lock:
            if task_queue:
                task_item = task_queue.pop(0)
        if task_item is not None:
            threading.Thread(target=download_task, args=task_item, daemon=True).start()
        time.sleep(0.2)


consumer_thread = threading.Thread(target=queue_consumer, daemon=True)
consumer_thread.start()


def enqueue_task(*args):
    with queue_lock:
        task_queue.append(args)


def safe_set_progress(task_id, obj):
    with store_lock:
        progress_store[task_id] = obj


def safe_get_progress(task_id):
    with store_lock:
        return progress_store.get(task_id, {
            "status": "unknown",
            "msg": "任务不存在",
            "video_percent": 0,
            "audio_percent": 0,
            "total_percent": 0,
        })


def download_task(url, format_code, save_name, task_id, write_subs):
    proc = None
    worker_semaphore.acquire()  # 阻塞直到有空闲槽位，实现真正的 MAX_WORKER 并发限制
    try:
        if not find_deno():
            safe_set_progress(task_id, {
                "status": "error",
                "msg": "❌ 缺少 deno 运行时，请将 deno.exe 放入程序目录或加入 PATH",
                "video_percent": 0, "audio_percent": 0, "total_percent": 0,
            })
            return

        # cookies.txt 变为可选：有则传给 yt-dlp，无则警告后继续（部分站点仍可下载）。
        cookies_ok = os.path.exists(COOKIE_FILE)
        safe_set_progress(task_id, {
            "status": "running",
            "msg": ("⚠️ 未找到 cookies.txt，部分网站可能失败或画质受限，继续尝试…"
                    if not cookies_ok else "🔍 开始解析视频..."),
            "video_percent": 0, "audio_percent": 0, "total_percent": 0,
        })

        cmd = [sys.executable, "-m", "yt_dlp", "--js-runtimes", "deno"]
        if cookies_ok:
            cmd += ["--cookies", COOKIE_FILE]
        if REMOTE_EJS:
            cmd += ["--remote-components", "ejs:github"]
        cmd += ["--no-continue",          # 有意禁用续传，避免半成品/损坏文件
                "--newline",               # 每条进度一行，便于逐行解析
                "--progress-template", PROGRESS_TMPL,
                "-f", format_code,
                "-o", build_output_template(save_name)]
        if write_subs:
            cmd += ["--write-subs", "--write-auto-subs", "--sub-format", "xml"]
        cmd.append(url)

        env = os.environ.copy()
        # 让 yt-dlp 能找到程序目录下的 deno.exe
        env["PATH"] = BASE_DIR + os.pathsep + env.get("PATH", "")

        proc = subprocess.Popen(
            cmd, cwd=BASE_DIR, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace",
        )
        with store_lock:
            proc_list.append(proc)

        pat_pct = re.compile(r"([\d.]+)%")
        video_p = 0.0
        audio_p = 0.0

        for raw in proc.stdout:
            line = raw.strip()
            if line.startswith("PROGRESS|"):
                parts = line.split("|", 3)
                pct_str = parts[2] if len(parts) > 2 else ""
                fname = parts[3] if len(parts) > 3 else ""
                m = pat_pct.search(pct_str)
                pct = float(m.group(1)) if m else 0.0
                ext = os.path.splitext(fname)[1].lower()
                if ext in AUDIO_EXTS:
                    audio_p = pct
                else:
                    video_p = pct
                safe_set_progress(task_id, {
                    "status": "running",
                    "msg": f"📥 下载中 视频:{video_p:.1f}% 音频:{audio_p:.1f}%",
                    "video_percent": video_p,
                    "audio_percent": audio_p,
                    "total_percent": (video_p + audio_p) / 2,
                })
                continue
            if "Merging" in line:
                safe_set_progress(task_id, {
                    "status": "running",
                    "msg": "🔧 正在合并音视频...",
                    "video_percent": 100, "audio_percent": 100, "total_percent": 100,
                })
                continue
            if "Writing subtitle" in line:
                safe_set_progress(task_id, {
                    "status": "running",
                    "msg": "📄 正在保存字幕/弹幕...",
                    "video_percent": video_p, "audio_percent": audio_p,
                    "total_percent": (video_p + audio_p) / 2,
                })
                continue

        ret = proc.wait()
        with store_lock:
            if proc in proc_list:
                proc_list.remove(proc)

        if ret == 0:
            safe_set_progress(task_id, {
                "status": "done",
                "msg": "✅ 下载完成！文件已保存到 downloads 文件夹",
                "video_percent": 100, "audio_percent": 100, "total_percent": 100,
            })
        else:
            safe_set_progress(task_id, {
                "status": "error",
                "msg": f"❌ yt-dlp 返回错误码:{ret}，链接或 Cookie 可能已失效",
                "video_percent": video_p, "audio_percent": audio_p,
                "total_percent": (video_p + audio_p) / 2,
            })

    except Exception as e:
        safe_set_progress(task_id, {
            "status": "error",
            "msg": f"💥 任务异常: {e}",
            "video_percent": 0, "audio_percent": 0, "total_percent": 0,
        })
        if proc is not None:
            try:
                kill_process_tree(proc.pid)
            except Exception:
                pass
        with store_lock:
            if proc and proc in proc_list:
                proc_list.remove(proc)
    finally:
        worker_semaphore.release()

        def delayed_clean(tid):
            time.sleep(600)  # 保留 10 分钟供前端轮询，之后清理
            with store_lock:
                progress_store.pop(tid, None)
        threading.Thread(target=delayed_clean, args=(task_id,), daemon=True).start()


@app.before_request
def check_auth():
    """本地接口鉴权：只允许携带正确 token 的请求调用 /start 与 /progress。"""
    if request.path in ("/start", "/open") or request.path.startswith("/progress/"):
        if request.headers.get("X-Auth-Token") != AUTH_TOKEN:
            return jsonify({"error": "forbidden"}), 403
    return None


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        auth_token=AUTH_TOKEN,
        ffmpeg_ok=find_ffmpeg() is not None,
        cookies_ok=os.path.exists(COOKIE_FILE),
    )


@app.route("/start", methods=["POST"])
def start_download():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"msg": "链接不能为空"}), 400
    fmt = data.get("format") or "bestvideo+bestaudio/best"
    name = (data.get("filename") or "").strip()
    write_subs = bool(data.get("writeSubs", False))
    task_id = str(uuid.uuid4())
    safe_set_progress(task_id, {
        "status": "queued",
        "msg": "⏳ 排队等待执行...",
        "video_percent": 0, "audio_percent": 0, "total_percent": 0,
    })
    enqueue_task(url, fmt, name, task_id, write_subs)
    return jsonify({"msg": "任务已加入队列", "task_id": task_id})


@app.route("/progress/<task_id>")
def get_progress(task_id):
    return jsonify(safe_get_progress(task_id))


@app.route("/open", methods=["POST"])
def open_download_folder():
    try:
        if hasattr(os, "startfile"):
            os.startfile(SAVE_ROOT)
        else:
            subprocess.Popen(["xdg-open", SAVE_ROOT])
        return jsonify({"msg": "ok"})
    except Exception as e:
        return jsonify({"msg": f"打开失败: {e}"}), 500


def start_server(port):
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)


def on_window_closed():
    """窗口关闭时只结束自己启动的下载进程树（不再全局强杀 ffmpeg/deno）。"""
    print("\n🔴 窗口关闭事件触发，终止所有下载子进程")
    with store_lock:
        for p in proc_list:
            try:
                kill_process_tree(p.pid)
            except Exception:
                pass
        proc_list.clear()
    print("✅ 所有子进程清理完成，准备退出主程序")
    exit_event.set()


if __name__ == "__main__":
    PORT = find_free_port(5000)  # 端口被占用时自动换一个，而不是静默失败
    flask_thread = threading.Thread(target=start_server, args=(PORT,), daemon=True)
    flask_thread.start()
    win = webview.create_window("视频下载器", f"http://127.0.0.1:{PORT}", width=1000, height=720)
    win.events.closed += on_window_closed
    webview.start()
    exit_event.wait()
    print("✅ 主程序完全退出")
    sys.exit(0)
