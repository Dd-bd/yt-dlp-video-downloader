@echo off
chcp 65001 >nul
title YT-DLP 视频下载器
cd /d "%~dp0"

set "PY=python"
where python >nul 2>nul
if errorlevel 1 set "PY=py"

rem ---- 检查依赖是否安装完整 ----
%PY% -c "import flask, webview, psutil, yt_dlp" >nul 2>nul
if errorlevel 1 (
    echo [提示] 依赖未安装完整，请先双击 install.bat 完成安装
    pause
    exit /b 1
)

rem ---- 检查 Cookie ----
if not exist "cookies.txt" (
    echo [提示] 未找到 cookies.txt，部分网站可能无法下载
    echo        请参考 README.md 的「导出 Cookie」一节，导出后放入本目录
    echo.
)

echo 正在启动，请稍候...
%PY% app.py
pause
