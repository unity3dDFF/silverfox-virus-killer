@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0build_windows.ps1"
if errorlevel 1 (
  echo Windows 打包失败。
  pause
  exit /b 1
)
echo Windows 打包完成，文件位于 dist 目录。
pause
