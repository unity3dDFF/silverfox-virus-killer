@echo off
chcp 65001 >nul
echo ==========================================
echo 银狐病毒专杀工具 - Windows打包脚本
echo SilverFox Virus Killer - Windows Build
echo ==========================================

:: 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python
    echo 请安装Python 3.8+: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到pip
    pause
    exit /b 1
)

:: 安装依赖
echo.
echo [1/4] 安装依赖...
pip install -r requirements.txt -q
pip install pyinstaller -q

if %errorlevel% neq 0 (
    echo 错误: 安装依赖失败
    pause
    exit /b 1
)

:: 清理旧文件
echo.
echo [2/4] 清理旧文件...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

:: 打包CLI版本
echo.
echo [3/4] 打包CLI版本...
pyinstaller --onefile --name SilverFoxKiller main.py

if %errorlevel% neq 0 (
    echo 错误: CLI打包失败
    pause
    exit /b 1
)

:: 打包GUI版本
echo.
echo [4/4] 打包GUI版本...
pyinstaller --onefile --windowed --name SilverFoxKillerGUI gui.py

if %errorlevel% neq 0 (
    echo 错误: GUI打包失败
    pause
    exit /b 1
)

:: 完成
echo.
echo ==========================================
echo 打包完成！
echo ==========================================
echo.
echo 输出文件:
echo   dist\SilverFoxKiller.exe     (命令行版本)
echo   dist\SilverFoxKillerGUI.exe  (图形界面版本)
echo.
echo 使用方法:
echo   双击 SilverFoxKillerGUI.exe 启动图形界面
echo   或打开命令行运行 SilverFoxKiller.exe
echo.
pause
