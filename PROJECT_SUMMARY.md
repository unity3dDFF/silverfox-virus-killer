# 银狐病毒专杀工具 - 项目总结

## 项目概述

银狐病毒专杀工具是一款专门针对"银狐"（SilverFox）木马病毒的查杀工具。该病毒是一种针对中国用户的远程控制木马，通过钓鱼消息传播，伪装成人事业务相关文件。

## 已完成的功能

### 1. 扫描模块 (scanner/)
- **文件扫描器** (file_scanner.py)：检测恶意文件名、哈希值、扩展名
- **注册表扫描器** (registry_scanner.py)：检测Run键、AppInit_DLLs等持久化位置
- **进程扫描器** (process_scanner.py)：检测可疑进程、异常路径、可疑命令行
- **网络扫描器** (network_scanner.py)：检测恶意域名、IP、端口

### 2. 清除模块 (cleaner/)
- **进程清除器** (process_cleaner.py)：终止恶意进程
- **文件清除器** (file_cleaner.py)：删除恶意文件
- **注册表清除器** (registry_cleaner.py)：清理恶意注册表项

### 3. 修复模块 (修复/)
- **系统修复器** (system_repair.py)：修复系统设置、安全配置、启动项、网络设置

### 4. 报告模块 (reports/)
- **报告生成器** (report_generator.py)：生成扫描、清除、修复报告

### 5. IOC数据库 (ioc/)
- **文件哈希** (file_hashes.py)：9个已知恶意文件哈希
- **域名列表** (domains.py)：9个恶意域名
- **注册表键** (registry_keys.py)：3个恶意注册表键位置
- **恶意文件** (files.py)：文件名、路径、扩展名
- **恶意进程** (processes.py)：进程名、路径、命令行模式
- **恶意IP** (ips.py)：已知恶意IP地址
- **恶意端口** (ports.py)：7个常见恶意端口

### 6. 工具函数 (utils/)
- **通用工具** (common.py)：文件哈希计算、备份、日志记录等

## 项目文件结构

```
yh/
├── main.py                    # 主程序入口
├── start.sh                  # 启动脚本
├── requirements.txt          # 依赖库
├── README.md                 # 项目说明
├── INSTALL.md               # 安装与使用指南
├── test_scanner.py           # 测试脚本
├── example_usage.py          # 使用示例
├── demo_ioc.py               # IOC数据库演示
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

## 使用方法

### 快速开始

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行扫描：
   ```bash
   python main.py scan
   ```

3. 清除病毒：
   ```bash
   python main.py clean
   ```

4. 修复系统：
   ```bash
   python main.py repair
   ```

5. 完整处理：
   ```bash
   python main.py full
   ```

### 使用启动脚本

```bash
./start.sh
```

然后按照菜单提示选择操作。

## 技术特点

### 跨平台支持
- **Windows**：完整支持（文件、注册表、进程、网络）
- **macOS/Linux**：部分支持（文件、进程、网络检测）

### 安全特性
- 操作前自动备份
- 详细的日志记录
- 完整的报告生成
- 错误处理和恢复

### 模块化设计
- 清晰的模块划分
- 易于扩展和维护
- 完整的IOC数据库

## 测试结果

所有测试均已通过：
- ✓ 模块导入测试
- ✓ 扫描器测试
- ✓ 清除器测试
- ✓ IOC数据库测试
- ✓ 报告生成器测试

## 项目统计

- **Python文件**：25个
- **模块数量**：6个主要模块
- **IOC指标**：
  - 文件哈希：9个
  - 恶意域名：9个
  - 恶意端口：7个
  - 注册表键：3个
- **代码行数**：约3000行

## 后续改进方向

1. **GUI界面**：添加图形用户界面
2. **实时监控**：实现实时文件和进程监控
3. **云端更新**：支持IOC数据库云端更新
4. **更多变种**：添加更多银狐病毒变种特征
5. **性能优化**：优化扫描和清除性能

## 免责声明

本工具仅供安全研究和防护使用。使用本工具所造成的任何后果，开发者不承担责任。

## 许可证

MIT License
