# 下载 ffmpeg essentials 版（约 80MB，静态单文件）到本脚本所在目录。
# 带重试 + 完整性校验：下载不完整的 zip 解压时会失败，自动重试。

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $MyInvocation.MyCommand.Path)

$url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
$ok = $false

Write-Host 'Downloading ffmpeg essentials build (about 80MB) ...'

for ($i = 1; $i -le 3 -and -not $ok; $i++) {
    try {
        Write-Host ("  Attempt {0}/3 ..." -f $i)
        Invoke-WebRequest -Uri $url -OutFile 'ffmpeg.zip' -UseBasicParsing
        Expand-Archive -LiteralPath 'ffmpeg.zip' -DestinationPath 'ffmpeg_tmp' -Force
        $exe = Get-ChildItem -LiteralPath 'ffmpeg_tmp' -Recurse -Filter 'ffmpeg.exe' -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($exe) {
            Copy-Item -LiteralPath $exe.FullName -Destination 'ffmpeg.exe' -Force
            $ok = $true
        } else {
            throw 'archive does not contain ffmpeg.exe'
        }
    } catch {
        Write-Host ("  Failed: " + $_.Exception.Message)
    } finally {
        Remove-Item -LiteralPath 'ffmpeg_tmp' -Recurse -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath 'ffmpeg.zip' -Force -ErrorAction SilentlyContinue
    }
}

if ($ok -and (Test-Path -LiteralPath 'ffmpeg.exe')) {
    $size = (Get-Item -LiteralPath 'ffmpeg.exe').Length
    Write-Host ("OK  ffmpeg.exe  {0:N1} MB" -f ($size / 1MB))
    if ($size -gt 100MB) {
        Write-Host 'WARNING: ffmpeg.exe exceeds 100MB, GitHub will reject the upload!'
    }
    exit 0
} else {
    Write-Host 'FAIL'
    exit 1
}
