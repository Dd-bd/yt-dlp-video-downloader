@echo off
title YT-DLP Video Downloader - Setup
cd /d "%~dp0"

echo ==============================================
echo   YT-DLP Video Downloader - One-click Setup
echo ==============================================
echo.

rem ---- 1. Check Python ----
set "PY=python"
where python >nul 2>nul
if errorlevel 1 set "PY=py"
where %PY% >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python first:
    echo   https://www.python.org/downloads/
    echo   IMPORTANT: check "Add Python to PATH" during install!
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found:
%PY% --version
echo.

rem ---- 2. Install Python dependencies ----
echo [1/3] Installing Python dependencies, please wait...
%PY% -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
%PY% -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo [ERROR] Dependency install failed. Check network and retry.
    pause
    exit /b 1
)
echo [1/3] Dependencies installed.
echo.

rem ---- 3. Download deno runtime ----
echo [2/3] Downloading deno runtime...
if exist "deno.exe" (
    echo deno.exe already exists, skip.
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; try { Invoke-WebRequest -Uri 'https://github.com/denoland/deno/releases/latest/download/deno-x86_64-pc-windows-msvc.zip' -OutFile 'deno.zip'; Expand-Archive -Path 'deno.zip' -DestinationPath 'deno_tmp' -Force; Copy-Item 'deno_tmp\deno.exe' 'deno.exe' -Force; Remove-Item 'deno_tmp' -Recurse -Force; Remove-Item 'deno.zip' -Force; Write-Host 'deno download OK' } catch { Write-Host ('deno download failed: ' + $_.Exception.Message) }"
    if exist "deno.exe" ( echo deno.exe downloaded. ) else ( echo [WARN] deno download failed. Re-run this script to retry. )
)
echo.

rem ---- 4. Check / download ffmpeg ----
echo [3/3] Checking ffmpeg...
where ffmpeg >nul 2>nul
if errorlevel 1 (
    if exist "ffmpeg.exe" (
        echo ffmpeg.exe found in program folder.
    ) else (
        echo ffmpeg not found. Downloading now (about 80MB, please wait)...
        powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0download_ffmpeg.ps1"
        if exist "ffmpeg.exe" (
            echo ffmpeg.exe downloaded.
        ) else (
            echo [WARN] ffmpeg auto-download failed. Download it manually and
            echo        put ffmpeg.exe into this folder:
            echo        https://www.gyan.dev/ffmpeg/builds/
        )
    )
) else (
    echo ffmpeg already installed on system.
)
echo.

echo ==============================================
echo   Setup done!
echo.
echo   Next steps (see README.md for details):
echo   1. Export browser cookies to cookies.txt in this folder
echo   2. Double-click start.bat to launch
echo ==============================================
pause
