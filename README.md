# YT-DLP 视频下载器

一个基于 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 的**图形化**视频下载工具，无需记命令，粘贴链接即可下载。

支持 **1800+ 网站**（YouTube、B站、抖音网页版、TikTok、Niconico 等），可下载视频、音频、弹幕/字幕，最高 4K。

> 目前仅支持 **Windows**。

---

## 功能特性

- 🎬 粘贴链接一键下载，支持一行一条**批量下载**
- 🎯 自选清晰度（最高 4K），自动合并最佳音视频
- 🎵 单独下载音频
- 📄 同时下载弹幕/字幕（xml 格式，B站弹幕可用）
- 📊 实时进度条（视频 / 音频双进度）
- ⏳ 最多 3 个任务并发下载，其余自动排队
- 🔑 Cookie 登录，可下载需登录/会员可看的内容

---

## 一、准备工作（只需做一次）

### 1. 安装 Python

1. 打开 <https://www.python.org/downloads/> 下载并安装 Python
2. ⚠️ 安装时**务必勾选底部 "Add Python to PATH"**，否则脚本找不到 Python

> 验证：按 `Win + R`，输入 `cmd` 回车，在黑色窗口输入 `python --version`，能显示版本号即成功。

### 2. 导出浏览器 Cookie（重要）

很多网站（YouTube、B站等）不登录就无法下载或只能下低清晰度。需要把浏览器登录状态导出成 `cookies.txt`：

1. 用 **Chrome 或 Edge** 浏览器，安装扩展 **"Get cookies.txt LOCALLY"**
   （Chrome 应用商店 / Edge 加载项里搜索即可）
2. 打开目标网站（如 YouTube）并**登录**
3. 点击浏览器右上角的扩展图标 → 点 **Export** → 保存文件
4. 把下载得到的文件改名为 **`cookies.txt`**，放到**本程序文件夹**（和 `app.py` 同级）

> 不会导出也没关系：不配置 Cookie 时，部分网站仍可下载，只是可能失败或画质受限。

---

## 二、快速开始

1. 双击 **`install.bat`** —— 自动安装依赖、下载 deno 和 ffmpeg（首次约需几分钟）
2. （建议）把 `cookies.txt` 放入本文件夹——YouTube/B站 等站点登录后可下更高画质
3. 双击 **`start.bat`** —— 弹出图形界面，粘贴链接即可下载

> 之后每次使用只需双击 `start.bat`。

---

## 三、界面使用说明

| 项目 | 说明 |
| --- | --- |
| 视频链接 | 粘贴链接，一行一条；支持播放列表链接（会下载整个列表） |
| 保存文件名 | 留空则自动使用视频标题；批量下载会自动加序号 `名称_1`、`名称_2` |
| 视频清晰度 | 选择想要的分辨率；若该视频没有对应清晰度会自动回退到最接近的 |
| 弹幕开关 | 打开后同时下载弹幕/字幕（xml） |
| 下载任务 | 显示每个任务的进度条、状态；完成后可点「打开文件夹」查看 |

下载的文件保存在程序文件夹下的 **`downloads`** 目录中。

---

## 四、常见问题（FAQ）

**Q1：双击 install.bat 一闪而过 / 提示找不到 Python？**
Python 未安装，或安装时没勾选 "Add Python to PATH"。重新安装 Python 并勾选该选项，或手动把 Python 加入系统 PATH。

**Q2：启动后窗口空白 / 打不开界面？**
通常是依赖没装完整。重新双击 `install.bat` 完成安装后再试。

**Q3：顶部出现「未找到 cookies.txt」的黄色提示？**
Cookie 是可选配置：不配置也能下载部分网站，但 YouTube、B站 等可能失败或画质受限。按上文「导出 Cookie」一节导出后放入本文件夹，重启程序即可消除提示。

**Q4：下载失败，提示「链接或 Cookie 可能已失效」？**
大概率是 Cookie 过期了（Cookie 一般几周内有效）。重新按上面步骤导出一份新的 `cookies.txt` 覆盖即可。

**Q5：选择 4K 但下载出来不是 4K？**
该视频本身没有 4K 版本，yt-dlp 会自动回退到最接近的清晰度。

**Q6：deno 或 ffmpeg 下载失败？**
手动下载：
- deno：<https://github.com/denoland/deno/releases>（下载 Windows 版 zip，解压出 `deno.exe` 放入本文件夹）
- ffmpeg：<https://www.gyan.dev/ffmpeg/builds/>（下载后解压，把 `bin\ffmpeg.exe` 放入本文件夹）

**Q7：端口被占用怎么办？**
程序会自动更换可用端口，无需处理。

---

## 五、进阶：打包成 exe（可选）

想发给完全不会用命令行的人，可以把程序打包成单个 exe：

```bat
pip install pyinstaller
pyinstaller app.spec
```

打包产物在 `dist\app.exe`。使用时需把 `cookies.txt`、`deno.exe`、`ffmpeg.exe` 放在 `app.exe` 同目录。

---

## 六、免责声明

- 本工具仅供**个人学习、备份自己有权访问的内容**使用。
- 请遵守目标网站的服务条款与当地法律法规，**勿下载受版权保护或未授权的内容**，勿用于商业用途。
- 下载行为产生的一切后果由使用者自行承担。

---

## 七、项目结构

```
yt-dlp-video-downloader/
├── app.py              # 主程序（Flask + pywebview 图形界面）
├── app.spec            # PyInstaller 打包配置
├── templates/          # 界面模板
│   └── index.html
├── requirements.txt    # Python 依赖清单
├── install.bat         # 一键安装（依赖 + deno + ffmpeg）
├── start.bat           # 启动脚本
├── icon.ico            # 程序图标
└── LICENSE             # MIT 许可证
```

## 许可

本项目（图形界面部分）采用 [MIT License](LICENSE)。底层下载能力由 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 提供。
