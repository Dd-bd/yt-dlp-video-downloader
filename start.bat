@echo off
title YT-DLP Video Downloader
cd /d "%~dp0"

set "PY=python"
where python >nul 2>nul
if errorlevel 1 set "PY=py"

rem ---- Check dependencies ----
%PY% -c "import flask, webview, psutil, yt_dlp" >nul 2>nul
if errorlevel 1 (
    echo [WARN] Dependencies not installed. Run install.bat first.
    pause
    exit /b 1
)

rem ---- Check cookies ----
if not exist "cookies.txt" (
    echo [WARN] cookies.txt not found. Some sites may fail to download.
    echo        See README.md "Export Cookie" section for help.
    echo.
)

rem ---- Check ffmpeg ----
where ffmpeg >nul 2>nul
if errorlevel 1 (
    if not exist "ffmpeg.exe" (
        echo [WARN] ffmpeg not found. 4K/merge will fall back to lower quality.
        echo        Run install.bat again, or put ffmpeg.exe in this folder.
        echo.
    )
)

echo Starting, please wait...
%PY% app.py
pause
