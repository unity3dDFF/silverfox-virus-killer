# 银狐病毒专杀工具

SilverFox Virus Killer - 专门针对银狐木马病毒的查杀工具

## 功能特性

- **全面扫描**: 文件系统、注册表、进程、网络连接全方位检测
- **智能清除**: 自动终止恶意进程、删除恶意文件、清理注册表
- **系统修复**: 恢复系统设置、修复安全配置、清理启动项
- **详细报告**: 生成详细的扫描、清除、修复报告
- **图形化界面**: 友好的GUI界面，操作简单直观

## 支持的威胁检测

### 银狐病毒特征
- **文件检测**: 检测已知的恶意文件名、哈希值、扩展名
- **注册表检测**: 检测Run键、AppInit_DLLs等持久化位置
- **进程检测**: 检测可疑进程、异常进程路径、可疑命令行
- **网络检测**: 检测恶意域名、IP地址、可疑端口

### 已知IOC（入侵指标）
- **文件哈希**: 20+ 个已知恶意文件哈希
- **恶意域名**: 阿里云OSS域名、其他恶意域名
- **恶意IP**: 已知的恶意IP地址
- **恶意端口**: 常见的恶意软件端口

## 安装与使用

### 环境要求
- Python 3.8+
- Windows 10/11（推荐）
- PyInstaller（打包exe时需要）

### 安装依赖
```bash
pip install -r requirements.txt
```

### 打包Windows exe

#### 方法1：使用批处理脚本（推荐）

```bash
# 双击运行
build_windows.bat
```

#### 方法2：手动打包

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包CLI版本
pyinstaller --onefile --name SilverFoxKiller main.py

# 打包GUI版本
pyinstaller --onefile --windowed --name SilverFoxKillerGUI gui.py
```

打包完成后，在 `dist` 目录下会生成：
- `SilverFoxKiller.exe` - 命令行版本
- `SilverFoxKillerGUI.exe` - 图形界面版本

详细打包说明请参考 [BUILD_WINDOWS.md](BUILD_WINDOWS.md)

### 使用方法

#### 图形化界面（推荐）

```bash
# 使用启动脚本
./start_gui.sh

# 或直接运行
python3 gui.py
```

#### 命令行方式

##### 扫描系统
```bash
python main.py scan
```

##### 清除病毒
```bash
python main.py clean
```

##### 修复系统
```bash
python main.py repair
```

##### 完整处理（扫描+清除+修复）
```bash
python main.py full
```

### 命令行参数
- `--verbose`, `-v`: 显示详细信息
- `--output`, `-o`: 指定报告输出文件（默认: report.txt）
- `--auto-fix`, `-a`: 自动修复发现的问题

## 项目结构

```
yh/
├── main.py                    # 主程序入口
├── gui.py                    # 图形化界面
├── version.py                # 版本信息
├── start.sh                  # 命令行启动脚本
├── start_gui.sh              # GUI启动脚本
├── build_windows.bat         # Windows打包脚本
├── SilverFoxKiller.spec      # PyInstaller配置（CLI）
├── SilverFoxKillerGUI.spec   # PyInstaller配置（GUI）
├── requirements.txt          # 依赖库
├── LICENSE                   # MIT许可证
├── .gitignore               # Git忽略文件
├── README.md                 # 项目说明
├── INSTALL.md               # 安装指南
├── QUICK_START.md           # 快速开始
├── PROJECT_SUMMARY.md       # 项目总结
├── COMPLETION_REPORT.md     # 完成报告
├── GUI_README.md            # GUI使用说明
├── GUI_SUMMARY.md           # GUI功能总结
├── BUILD_WINDOWS.md         # Windows打包说明
├── scanner/                  # 扫描模块
│   ├── __init__.py
│   ├── file_scanner.py      # 文件扫描
│   ├── registry_scanner.py  # 注册表扫描
│   ├── process_scanner.py   # 进程扫描
│   └── network_scanner.py   # 网络扫描
├── cleaner/                  # 清除模块
│   ├── __init__.py
│   ├── process_cleaner.py   # 进程清除
│   ├── file_cleaner.py      # 文件清除
│   └── registry_cleaner.py  # 注册表清理
├── 修复/                     # 修复模块
│   ├── __init__.py
│   └── system_repair.py     # 系统修复
├── reports/                  # 报告模块
│   ├── __init__.py
│   └── report_generator.py  # 报告生成
├── ioc/                      # IOC数据库
│   ├── __init__.py
│   ├── file_hashes.py       # 文件哈希
│   ├── domains.py           # 域名列表
│   ├── registry_keys.py     # 注册表键
│   ├── files.py             # 恶意文件
│   ├── processes.py         # 恶意进程
│   ├── ips.py               # 恶意IP
│   └── ports.py             # 恶意端口
└── utils/                    # 工具函数
    ├── __init__.py
    └── common.py            # 通用工具
```

## 技术特点

### 检测技术
- **多维度检测**: 文件、注册表、进程、网络全方位覆盖
- **特征匹配**: 基于已知恶意特征的快速检测
- **行为分析**: 检测可疑的行为模式
- **哈希验证**: 基于文件哈希的精确检测

### 清除技术
- **进程终止**: 安全终止恶意进程
- **文件删除**: 删除恶意文件和目录
- **注册表清理**: 清理恶意注册表项
- **系统修复**: 恢复被篡改的系统设置

### 图形化界面
- **友好界面**: 直观的GUI设计，操作简单
- **实时进度**: 进度条实时显示操作进度
- **结果表格**: 扫描结果以表格形式清晰展示
- **详细日志**: 所有操作记录在日志区域
- **异步操作**: 后台线程执行，保持界面响应
- **跨平台**: 支持Windows、macOS、Linux

### 安全特性
- **备份机制**: 操作前自动备份重要文件
- **权限检查**: 检查操作权限，避免误操作
- **日志记录**: 详细记录所有操作
- **报告生成**: 生成详细的处理报告

## 更新与维护

### IOC更新
定期更新IOC数据库，添加新发现的恶意特征：
- 文件哈希
- 恶意域名
- IP地址
- 注册表键

### 版本更新
- 定期检查更新
- 修复已知问题
- 添加新功能

## 注意事项

1. **管理员权限**: 某些操作需要管理员权限
2. **备份重要数据**: 使用前建议备份重要数据
3. **隔离环境测试**: 建议在隔离环境中先测试
4. **网络连接**: 某些功能需要网络连接

## 免责声明

本工具仅供安全研究和防护使用。使用本工具所造成的任何后果，开发者不承担责任。

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过GitHub Issues反馈。
