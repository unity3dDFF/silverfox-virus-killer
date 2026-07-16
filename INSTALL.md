# 银狐病毒专杀工具 - 安装与使用指南

## 项目概述

银狐病毒专杀工具是一款专门针对"银狐"（SilverFox）木马病毒的查杀工具。该病毒是一种针对中国用户的远程控制木马，通过钓鱼消息传播，伪装成人事业务相关文件。

## 快速开始

### 1. 环境要求

- Python 3.8 或更高版本
- Windows 10/11（推荐）
- 管理员权限（某些功能需要）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或使用启动脚本（自动安装依赖）：

```bash
./start.sh
```

### 3. 使用方法

#### 命令行方式

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

#### 启动脚本方式

```bash
./start.sh
```

然后按照菜单提示选择操作。

## 功能详解

### 1. 扫描功能 (scan)

**检测内容：**
- 恶意文件（文件名、哈希值、扩展名）
- 恶意注册表项（Run键、AppInit_DLLs等）
- 可疑进程（异常路径、可疑命令行）
- 恶意网络连接（恶意域名、IP、端口）

**使用示例：**
```bash
python main.py scan --verbose --output scan_report.txt
```

### 2. 清除功能 (clean)

**清除内容：**
- 终止恶意进程
- 删除恶意文件
- 清理恶意注册表项
- 阻止恶意网络连接

**使用示例：**
```bash
python main.py clean --verbose --output clean_report.txt
```

### 3. 修复功能 (repair)

**修复内容：**
- 恢复Windows更新服务
- 恢复Windows Defender服务
- 修复系统文件
- 修复防火墙设置
- 修复UAC设置
- 清理恶意启动项
- 修复DNS设置
- 修复hosts文件

**使用示例：**
```bash
python main.py repair --verbose --output repair_report.txt
```

### 4. 完整处理 (full)

执行完整的扫描、清除、修复流程。

**使用示例：**
```bash
python main.py full --verbose --output full_report.txt
```

## IOC数据库

项目包含以下IOC（入侵指标）数据库：

### 文件哈希
- 已知的银狐病毒变种哈希值
- 持续更新中

### 恶意域名
- 阿里云OSS域名：`omss.oss-cn-hangzhou.aliyuncs.com`
- 其他恶意域名：`vauwjw.net`, `cinskw.net`, `hucgiu.net`

### 恶意注册表键
- Run键持久化位置
- AppInit_DLLs位置

### 恶意文件
- 常见恶意文件名：`开票-目录.exe`, `违规-告示.exe`
- 常见恶意文件路径

## 技术特点

### 跨平台支持
- Windows：完整支持（文件、注册表、进程、网络）
- macOS/Linux：部分支持（文件、进程、网络检测）

### 安全特性
- 操作前自动备份
- 详细的日志记录
- 完整的报告生成
- 错误处理和恢复

### 模块化设计
- 扫描模块 (scanner/)
- 清除模块 (cleaner/)
- 修复模块 (修复/)
- 报告模块 (reports/)
- IOC数据库 (ioc/)
- 工具函数 (utils/)

## 常见问题

### Q: 为什么某些功能在macOS上不可用？
A: 注册表操作和某些Windows系统命令（如sc、netsh、sfc）是Windows特有的，在其他操作系统上会自动跳过。

### Q: 如何更新IOC数据库？
A: 编辑 `ioc/` 目录下的相应文件，添加新的IOC指标。

### Q: 如何生成自定义报告？
A: 使用 `--output` 参数指定输出文件，报告会自动生成为文本格式。

### Q: 工具需要管理员权限吗？
A: 扫描功能不需要，但某些清除和修复功能可能需要管理员权限。

## 开发与贡献

### 项目结构

```
yh/
├── main.py                    # 主程序入口
├── scanner/                  # 扫描模块
│   ├── file_scanner.py      # 文件扫描
│   ├── registry_scanner.py  # 注册表扫描
│   ├── process_scanner.py   # 进程扫描
│   └── network_scanner.py   # 网络扫描
├── cleaner/                  # 清除模块
│   ├── process_cleaner.py   # 进程清除
│   ├── file_cleaner.py      # 文件清除
│   └── registry_cleaner.py  # 注册表清理
├── 修复/                     # 修复模块
│   └── system_repair.py     # 系统修复
├── reports/                  # 报告模块
│   └── report_generator.py  # 报告生成
├── ioc/                      # IOC数据库
│   ├── file_hashes.py       # 文件哈希
│   ├── domains.py           # 域名列表
│   ├── registry_keys.py     # 注册表键
│   ├── files.py             # 恶意文件
│   ├── processes.py         # 恶意进程
│   ├── ips.py               # 恶意IP
│   └── ports.py             # 恶意端口
└── utils/                    # 工具函数
    └── common.py            # 通用工具
```

### 运行测试

```bash
python test_scanner.py
```

## 注意事项

1. **备份重要数据**：使用前建议备份重要数据
2. **管理员权限**：某些操作需要管理员权限
3. **隔离环境测试**：建议在隔离环境中先测试
4. **持续更新**：IOC数据库需要持续更新

## 免责声明

本工具仅供安全研究和防护使用。使用本工具所造成的任何后果，开发者不承担责任。

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过GitHub Issues反馈。
