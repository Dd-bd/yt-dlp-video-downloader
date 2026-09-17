# YT-DLP Video Downloader · YT-DLP 视频下载器

A **graphical** video download tool based on [yt-dlp](https://github.com/yt-dlp/yt-dlp) — no commands to memorize, just paste a link and download.

一个基于 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 的**图形化**视频下载工具，无需记命令，粘贴链接即可下载。

Supports **1800+ sites** (YouTube, Bilibili, Douyin web, TikTok, Niconico, etc.). Download video, audio, and danmaku/subtitles, up to **4K**.

支持 **1800+ 网站**（YouTube、B站、抖音网页版、TikTok、Niconico 等），可下载视频、音频、弹幕/字幕，最高 **4K**。

> Currently supports **Windows** only, and requires **Python 3.8 or newer**.

> 目前仅支持 **Windows**，需 **Python 3.8 及以上**。

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![yt-dlp](https://img.shields.io/badge/Powered_by-yt--dlp-orange)](https://github.com/yt-dlp/yt-dlp)

---

## Features · 功能特性

- 🎬 Paste links to download with one click; supports **batch download** (one link per line, including playlists) 
-    粘贴链接一键下载，支持一行一条**批量下载**（含播放列表）
- 🎯 Choose resolution (up to 4K) and auto-merge the best audio/video 
-    自选清晰度（最高 4K），自动合并最佳音视频
- 🎵 Download audio only 
-    单独下载音频
- 📄 Download danmaku/subtitles at the same time (xml format, works for Bilibili danmaku)
-    同时下载弹幕/字幕（xml 格式，B站弹幕可用）
- 📊 Real-time progress bar (dual progress for video / audio)
-    实时进度条（视频 / 音频双进度）
- ⏳ Up to 3 concurrent downloads, the rest are queued automatically
-    最多 3 个任务并发下载，其余自动排队
- 🔑 Cookie login to download content that requires login/membership
-    Cookie 登录，可下载需登录/会员可看的内容

---

## Requirements · 环境要求

| Dependency · 依赖 | Description · 说明 |
| --- | --- |
| Python 3.8+ | Required; check "Add Python to PATH" during installation / 必须，安装时勾选 "Add Python to PATH" |
| deno | Auto-downloaded to the program folder by `install.bat` / `install.bat` 自动下载到程序目录 |
| ffmpeg | Auto-downloaded to the program folder by `download_ffmpeg.bat` / `download_ffmpeg.bat` 自动下载到程序目录 |
| cookies.txt | Optional but strongly recommended (required for high quality on YouTube/Bilibili) / 可选，强烈建议（YouTube/B站 高画质必需） |

> Both `deno.exe` and `ffmpeg.exe` are **downloaded automatically** to the program folder by the scripts — no manual preparation needed. If a download fails due to network issues, see the FAQ below.

> `deno.exe` 和 `ffmpeg.exe` 都会由脚本**自动下载**到程序文件夹，无需手动准备；如网络原因下载失败，见下方 FAQ。

---

## Quick Start · 快速开始

### 1. Get the program · 获取程序

- **Release users** / **Release 用户**: Go to the **Releases** page on the right side of the repo, download the latest **Source code (zip)**, and extract it to any folder. 
- 到仓库右侧 **Releases** 页面下载最新版 **Source code (zip)**，解压到任意文件夹。
- **Developers** / **开发者**: `git clone` this repository. / `git clone` 本仓库。

### 2. Install Python · 装好 Python

Open <https://www.python.org/downloads/> to download and install it. ⚠️ **Make sure to check "Add Python to PATH"** at the bottom during installation.

打开 <https://www.python.org/downloads/> 下载安装，⚠️ 安装时**务必勾选底部 "Add Python to PATH"**。

> Verify / 验证: press `Win + R`, type `cmd` and press Enter, then run `python --version`. If a version number is shown, it's ready.
> 按 `Win + R` 输入 `cmd` 回车，输入 `python --version`，能显示版本号即成功。

### 3. One-click install · 一键安装

Double-click **`install.bat` and `download_ffmpeg.bat`**; they will do three things automatically (the first run takes a few minutes):

双击 **`install.bat`和`download_ffmpeg.bat`**，会自动完成三件事（首次约需几分钟）：

1. Install Python dependencies (`yt-dlp`, `flask`, `pywebview`, `psutil`)
   安装 Python 依赖（`yt-dlp`、`flask`、`pywebview`、`psutil`）
2. Download `deno.exe` (yt-dlp's JS runtime)
   下载 `deno.exe`（yt-dlp 的 JS 运行时）
3. Download `ffmpeg.exe` (used to merge audio/video)
   下载 `ffmpeg.exe`（用于合并音视频）

### 4. Launch · 启动

Double-click **`start.bat`**; the GUI opens and you can paste a link to download. From then on, just double-click `start.bat` each time.

双击 **`start.bat`**，弹出图形界面，粘贴链接即可下载。之后每次使用只需双击 `start.bat`。

---

## Export browser cookies (important) · 导出浏览器 Cookie（重要）

Many sites (YouTube, Bilibili, etc.) won't let you download, or only offer low quality, unless you're logged in. Export your browser login state to `cookies.txt`:

很多网站（YouTube、B站等）不登录就无法下载或只能下低清晰度。需要把浏览器登录状态导出成 `cookies.txt`：

1. In **Chrome or Edge**, install the **"Get cookies.txt LOCALLY"** extension (search for it in the store)
   用 **Chrome 或 Edge**，安装扩展 **"Get cookies.txt LOCALLY"**（应用商店搜索即可）
2. Open the target site (e.g. YouTube) and **log in**
   打开目标网站（如 YouTube）并**登录**
3. Click the extension icon → **Export** → save the file
   点击扩展图标 → **Export** → 保存文件
4. Rename the file to **`cookies.txt`** and put it in **the program folder** (same level as `app.py`)
   把文件改名为 **`cookies.txt`**，放到**本程序文件夹**（和 `app.py` 同级）

> You can still download from some sites without a Cookie, but it may fail or be limited in quality.

> 不配置 Cookie 也能下载部分网站，只是可能失败或画质受限。

---

## Interface guide · 界面使用说明

| Item · 项目 | Description · 说明 |
| --- | --- |
| Video links / 视频链接 | Paste links, one per line; playlist links are supported (the whole list is downloaded)
粘贴链接，一行一条；支持播放列表链接（会下载整个列表） |
| Filename / 保存文件名 | Leave blank to use the video title; batch downloads get a number suffix like `name_1`, `name_2`
留空则自动使用视频标题；批量下载会自动加序号 `名称_1`、`名称_2` |
| Resolution / 视频清晰度 | Choose a resolution; if the video lacks it, it falls back to the closest one
选择分辨率；视频没有该清晰度时会自动回退到最接近的 |
| Danmaku toggle / 弹幕开关 | When on, danmaku/subtitles (xml) are downloaded too
打开后同时下载弹幕/字幕（xml） |
| Download tasks / 下载任务 | Shows each task's progress and status; click "Open folder" when done
显示每个任务的进度、状态；完成后可点「打开文件夹」查看 |

Downloaded files are saved in the **`downloads`** folder inside the program folder.
下载的文件保存在程序文件夹下的 **`downloads`** 目录中。

---

## FAQ · 常见问题

**Q1: install.bat flashes and closes / says Python can't be found? · 双击 install.bat 一闪而过 / 提示找不到 Python？**

Python isn't installed, or "Add Python to PATH" wasn't checked. Reinstall and check it, or add Python to your system PATH manually.
Python 未安装，或安装时没勾选 "Add Python to PATH"。重新安装并勾选，或手动把 Python 加入系统 PATH。

**Q2: The window is blank / the interface won't open after launch? · 启动后窗口空白 / 打不开界面？**

Usually the dependencies weren't fully installed. Double-click `install.bat` and `download_ffmpeg.bat` again to finish the install, then retry.
通常是依赖没装完整。重新双击 `install.bat`和`download_ffmpeg.bat` 完成安装后再试。

**Q3: A yellow "cookies.txt not found" notice appears at the top? · 顶部出现「未找到 cookies.txt」的黄色提示？**

Cookies are optional: you can still download from some sites, but YouTube, Bilibili, etc. may fail or be quality-limited. Export the Cookie as described above, put it in this folder, and restart the program to remove the notice.
Cookie 是可选配置：不配置也能下载部分网站，但 YouTube、B站 等可能失败或画质受限。按上文「导出 Cookie」导出后放入本文件夹，重启程序即可消除提示。

**Q4: Download fails with "link or Cookie may have expired"? · 下载失败，提示「链接或 Cookie 可能已失效」？**

Most likely the Cookie has expired (Cookies generally last a few weeks). Export a fresh `cookies.txt` and overwrite the old one.
大概率是 Cookie 过期了（Cookie 一般几周内有效）。重新导出一份新的 `cookies.txt` 覆盖即可。

**Q5: I chose 4K but the download isn't 4K? · 选择 4K 但下载出来不是 4K？**

That video has no 4K version; yt-dlp falls back to the closest resolution automatically.
该视频本身没有 4K 版本，yt-dlp 会自动回退到最接近的清晰度。

**Q6: deno or ffmpeg failed to download? · deno 或 ffmpeg 下载失败？**

- ffmpeg: double-click `download_ffmpeg.bat` to re-download it alone (with retries and integrity check), or manually download the "release essentials" package from <https://www.gyan.dev/ffmpeg/builds/> and put `bin\ffmpeg.exe` into this folder.
- 双击 `download_ffmpeg.bat` 单独重下（带重试和完整性校验），或手动下载 <https://www.gyan.dev/ffmpeg/builds/> 的 "release essentials" 包，把 `bin\ffmpeg.exe` 放入本文件夹。
- deno: double-click `install.bat` to retry, or manually download from <https://github.com/denoland/deno/releases> (Windows zip; extract `deno.exe` into this folder).
- 重新双击 `install.bat` 重试，或手动下载 <https://github.com/denoland/deno/releases>（Windows 版 zip，解压出 `deno.exe` 放入本文件夹）。
- You can also install with winget: `winget install DenoLand.Deno`, `winget install Gyan.FFmpeg`.
- 也可用 winget 一键安装：`winget install DenoLand.Deno`、`winget install Gyan.FFmpeg`。

**Q7: What if the port is already in use? · 端口被占用怎么办？**

The program picks another available port automatically — no action needed.
程序会自动更换可用端口，无需处理。

---

## Advanced: package as an exe (optional) · 进阶：打包成 exe（可选）

To share with people who can't use the command line at all, you can package the program into a single exe:
想发给完全不会用命令行的人，可以把程序打包成单个 exe：

```bat
pip install pyinstaller
pyinstaller app.spec
```

The output is at `dist\app.exe`. Place `cookies.txt`, `deno.exe`, and `ffmpeg.exe` in the same directory as `app.exe` when using it.
打包产物在 `dist\app.exe`。使用时需把 `cookies.txt`、`deno.exe`、`ffmpeg.exe` 放在 `app.exe` 同目录。

---

## Project structure · 项目结构

```
yt-dlp-video-downloader/
├── app.py                  # Main program (Flask + pywebview GUI) / 主程序（Flask + pywebview 图形界面）
├── app.spec                # PyInstaller build config / PyInstaller 打包配置
├── templates/              # UI templates / 界面模板
│   └── index.html
├── requirements.txt        # Python dependencies list / Python 依赖清单
├── install.bat             # One-click install (deps + deno + ffmpeg) / 一键安装（依赖 + deno + ffmpeg）
├── start.bat               # Launch script / 启动脚本
├── download_ffmpeg.bat     # One-click script to download ffmpeg only / 单独下载 ffmpeg 的一键脚本
├── download_ffmpeg.ps1     # ffmpeg download logic (called by install.bat) / ffmpeg 下载逻辑（被 install.bat 调用）
├── icon.ico                # Program icon / 程序图标
└── LICENSE                 # MIT License / MIT 许可证
```

---

## Disclaimer · 免责声明

- This tool is for **personal study and backing up content you are authorized to access** only.
- 本工具仅供**个人学习、备份自己有权访问的内容**使用。
- Please comply with the target sites' terms of service and local laws and regulations. **Do not download copyrighted or unauthorized content**, and do not use it commercially.
- 请遵守目标网站的服务条款与当地法律法规，**勿下载受版权保护或未授权的内容**，勿用于商业用途。
- Users take full responsibility for any consequences of downloading.
- 下载行为产生的一切后果由使用者自行承担。

---

## License · 许可

This project (the GUI part) is licensed under the [MIT License](LICENSE). The underlying download capability is powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp).
本项目（图形界面部分）采用 [MIT License](LICENSE)。底层下载能力由 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 提供。
