@echo off
chcp 65001 >nul
title 一键安装 - YT-DLP 视频下载器
cd /d "%~dp0"

echo ==============================================
echo   YT-DLP 视频下载器 - 依赖一键安装
echo ==============================================
echo.

rem ---- 1. 检查 Python ----
set "PY=python"
where python >nul 2>nul
if errorlevel 1 set "PY=py"
where %PY% >nul 2>nul
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装：
    echo   下载地址：https://www.python.org/downloads/
    echo   安装时务必勾选 "Add Python to PATH"！
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [检查] 已找到 Python：
%PY% --version
echo.

rem ---- 2. 安装 Python 依赖（清华镜像加速）----
echo [1/3] 正在安装 Python 依赖库，请稍候...
%PY% -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
%PY% -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo [错误] 依赖安装失败，请检查网络后重新运行本脚本
    pause
    exit /b 1
)
echo [1/3] Python 依赖安装完成
echo.

rem ---- 3. 下载 deno 运行时 ----
echo [2/3] 正在下载 deno 运行时（用于解析视频签名）...
if exist "deno.exe" (
    echo deno.exe 已存在，跳过
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; try { Invoke-WebRequest -Uri 'https://github.com/denoland/deno/releases/latest/download/deno-x86_64-pc-windows-msvc.zip' -OutFile 'deno.zip'; Expand-Archive -Path 'deno.zip' -DestinationPath 'deno_tmp' -Force; Copy-Item 'deno_tmp\deno.exe' 'deno.exe' -Force; Remove-Item 'deno_tmp' -Recurse -Force; Remove-Item 'deno.zip' -Force; Write-Host 'deno download OK' } catch { Write-Host ('deno download failed: ' + $_.Exception.Message) }"
    if exist "deno.exe" ( echo deno.exe 下载完成 ) else ( echo [提示] deno 下载失败，稍后可重新运行本脚本重试 )
)
echo.

rem ---- 4. 检查 / 下载 ffmpeg ----
echo [3/3] 正在检查 ffmpeg（用于合并音视频）...
where ffmpeg >nul 2>nul
if errorlevel 1 (
    if exist "ffmpeg.exe" (
        echo 已找到程序目录下的 ffmpeg.exe
    ) else (
        echo 未检测到 ffmpeg，正在自动下载（约 80MB，请耐心等待）...
        powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; try { Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip'; Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'ffmpeg_tmp' -Force; $exe=(Get-ChildItem 'ffmpeg_tmp' -Recurse -Filter 'ffmpeg.exe')[0]; Copy-Item $exe.FullName 'ffmpeg.exe' -Force; Remove-Item 'ffmpeg_tmp' -Recurse -Force -ErrorAction SilentlyContinue; Remove-Item 'ffmpeg.zip' -Force -ErrorAction SilentlyContinue; Write-Host 'ffmpeg download OK' } catch { Write-Host ('ffmpeg download failed: ' + $_.Exception.Message) }"
        if exist "ffmpeg.exe" (
            echo ffmpeg.exe 下载完成
        ) else (
            echo [提示] ffmpeg 自动下载失败，可手动下载 ffmpeg.exe 放入本目录
            echo        下载地址：https://www.gyan.dev/ffmpeg/builds/
        )
    )
) else (
    echo 已检测到系统已安装 ffmpeg
)
echo.

echo ==============================================
echo   安装完成！
echo.
echo   接下来只需两步：
echo   1. 导出浏览器 Cookie 保存为 cookies.txt 放入本目录
echo      （方法见 README.md，不导出则部分网站无法下载）
echo   2. 双击 start.bat 启动下载器
echo ==============================================
pause
