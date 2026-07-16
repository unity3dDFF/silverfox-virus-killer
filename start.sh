#!/bin/bash
# 银狐病毒专杀工具启动脚本
# SilverFox Virus Killer Launcher Script

echo "=========================================="
echo "银狐病毒专杀工具 v1.0"
echo "SilverFox Virus Killer v1.0"
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

# 显示菜单
echo ""
echo "请选择操作:"
echo "1. 扫描系统 (scan)"
echo "2. 清除病毒 (clean)"
echo "3. 修复系统 (repair)"
echo "4. 完整处理 (full)"
echo "5. 运行测试"
echo "6. 退出"
echo ""

read -p "请输入选项 [1-6]: " choice

case $choice in
    1)
        echo "开始扫描..."
        python3 main.py scan
        ;;
    2)
        echo "开始清除..."
        python3 main.py clean
        ;;
    3)
        echo "开始修复..."
        python3 main.py repair
        ;;
    4)
        echo "开始完整处理..."
        python3 main.py full
        ;;
    5)
        echo "运行测试..."
        python3 test_scanner.py
        ;;
    6)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac
