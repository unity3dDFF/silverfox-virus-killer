#!/bin/bash
# 银狐病毒专杀工具 - GUI启动脚本
# SilverFox Virus Killer - GUI Launcher Script

echo "=========================================="
echo "银狐病毒专杀工具 v1.0 - 图形化界面"
echo "SilverFox Virus Killer v1.0 - GUI"
echo "=========================================="

# 检查Python版本
python3 --version 2>/dev/null || {
    echo "错误: 未找到Python3"
    echo "请安装Python3: https://www.python.org/downloads/"
    exit 1
}

# 检查依赖
echo "检查依赖..."
pip3 install psutil -q 2>/dev/null

# 启动GUI
echo "启动图形化界面..."
python3 gui.py
