# 银狐病毒专杀工具 - 快速开始

## 一键安装

```bash
# 克隆或下载项目后，进入项目目录
cd yh

# 安装依赖
pip install -r requirements.txt
```

## 快速使用

### 方法1：使用启动脚本（推荐）

```bash
./start.sh
```

然后按照菜单提示选择操作。

### 方法2：命令行直接使用

```bash
# 扫描系统
python main.py scan

# 清除病毒
python main.py clean

# 修复系统
python main.py repair

# 完整处理（扫描+清除+修复）
python main.py full
```

### 方法3：使用示例

```bash
# 运行完整示例
python example_usage.py

# 运行IOC数据库演示
python demo_ioc.py

# 运行测试
python test_scanner.py
```

## 常用命令

### 扫描并生成报告

```bash
python main.py scan --output scan_report.txt
```

### 详细模式扫描

```bash
python main.py scan --verbose
```

### 完整处理并生成报告

```bash
python main.py full --verbose --output full_report.txt
```

## 检测内容

### 文件检测
- 恶意文件名：`开票-目录.exe`, `违规-告示.exe`等
- 恶意文件哈希：9个已知恶意哈希
- 可疑文件扩展名：.dll, .exe, .msi等

### 注册表检测（Windows）
- Run键持久化
- AppInit_DLLs

### 进程检测
- 可疑进程路径
- 可疑命令行参数

### 网络检测
- 恶意域名：vauwjw.net, cinskw.net等
- 恶意端口：8880, 4444等

## 注意事项

1. **Windows系统**：所有功能完整支持
2. **macOS/Linux**：部分功能（注册表、系统修复）会自动跳过
3. **管理员权限**：某些清除和修复功能可能需要
4. **备份数据**：使用前建议备份重要数据

## 故障排除

### 问题：找不到Python
**解决**：安装Python 3.8+：https://www.python.org/downloads/

### 问题：权限错误
**解决**：使用管理员权限运行，或使用sudo（Linux/macOS）

### 问题：模块导入错误
**解决**：运行 `pip install -r requirements.txt` 安装依赖

## 获取帮助

```bash
# 查看帮助
python main.py --help

# 查看详细文档
cat README.md
cat INSTALL.md
```

## 技术支持

如有问题，请查看：
- README.md - 项目说明
- INSTALL.md - 安装指南
- PROJECT_SUMMARY.md - 项目总结
