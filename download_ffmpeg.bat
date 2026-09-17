@echo off
title FFmpeg Essentials Download
cd /d "%~dp0"

echo ==============================================
echo   FFmpeg Essentials Downloader (about 80MB)
echo ==============================================
echo.
echo Downloading... this may take a few minutes.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0download_ffmpeg.ps1"

echo.
if exist "ffmpeg.exe" (
    echo ==============================================
    echo   Success. ffmpeg.exe is now in this folder.
    echo ==============================================
) else (
    echo ==============================================
    echo   Download failed. Manual download:
    echo     https://www.gyan.dev/ffmpeg/builds/
    echo   Get the "release essentials" zip, then put
    echo   bin\ffmpeg.exe into this folder.
    echo ==============================================
)
echo.
pause
