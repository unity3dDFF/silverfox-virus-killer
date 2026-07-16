# 银狐病毒专杀工具

面向 Windows 10/11 的银狐木马检测与保守处置工具。v1.0.4 的核心原则是：**证据分级、默认不误删、确认 IOC 才处置、文件先隔离且可恢复**。

## Windows 版本

`dist` 目录包含：

- `SilverFoxKillerGUI-v1.0.4-windows-x64.exe`：图形界面，适合普通用户。
- `SilverFoxKiller-v1.0.4-windows-x64.exe`：命令行版本，适合应急响应与批量采集。
- `SHA256SUMS-v1.0.4.txt`：发布物完整性校验值。

扫描可以普通权限运行；注册表、系统级进程和安全设置修复需要管理员权限。

## v1.0.4 能力

- 扫描常见投递目录、启动项、运行进程与活动网络连接。
- GUI 使用候选文件总数和实际完成阶段驱动进度，不再模拟百分比。
- 新版界面提供风险/置信度分栏、概览卡片、彩色结果、隔离恢复和报告导出。
- 同时计算 MD5、SHA-1、SHA-256，兼容不同年代的公开 IOC。
- 结果包含 `severity`、`confidence`、`detector` 和证据详情。
- 只有已知哈希精确命中才标记为 `confirmed` 并允许自动处置。
- 文件移动到本机隔离区，改为不可执行扩展名，并记录 SHA-256、原路径和恢复 ID。
- 终止进程前校验 PID、创建时间、路径，并拒绝终止 Windows 核心进程。
- 注册表值只有在目标文件哈希确认后才清理，操作前写入备份。
- 网络端口仅作为低置信线索；工具不会谎报“已阻止”连接。
- 系统修复限于启用 Windows 防火墙/Defender、刷新 DNS、备份后清理 hosts 精确 IOC；WDAC 只审计不自动删除。

## 使用

```powershell
# 扫描并生成文本报告
.\SilverFoxKiller-v1.0.4-windows-x64.exe scan --output report.txt

# 只扫描指定目录（进程、注册表和网络仍会检查）
.\SilverFoxKiller-v1.0.4-windows-x64.exe scan --path C:\Users\Public\Downloads --json

# 重新扫描并处置已确认 IOC；启发式结果会跳过
.\SilverFoxKiller-v1.0.4-windows-x64.exe clean --yes --output clean-report.txt

# 查看隔离区
.\SilverFoxKiller-v1.0.4-windows-x64.exe quarantine-list

# 恢复隔离文件
.\SilverFoxKiller-v1.0.4-windows-x64.exe restore --id <隔离ID> --yes

# 保守系统修复
.\SilverFoxKiller-v1.0.4-windows-x64.exe repair --yes
```

不带 `--yes` 时，CLI 不会执行修改系统的操作。GUI 在处置前显示确认对话框。

隔离和备份默认位于 `%ProgramData%\SilverFoxKiller`；无该环境变量时回退到当前用户数据目录。样本不会上传。

## 从源码运行与测试

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python main.py scan
python gui.py
```

## 构建 Windows EXE

```powershell
.\build_windows.ps1
```

也可双击 `build_windows.bat`。打 `v*` 标签或手动触发 GitHub Actions 会构建 CLI、GUI 和校验文件。详见 [BUILD_WINDOWS.md](BUILD_WINDOWS.md)。

## 检测边界

- 文件名、所在目录、脚本宿主、端口和启动项名称都可能是合法行为，只作为线索。
- IOC 会过期或被云服务复用，处置前仍应结合数字签名、来源、时间线和企业资产基线复核。
- 本工具不是通用杀毒软件，不能替代 Microsoft Defender、EDR 或离线应急盘。
- 不要通过关闭杀毒软件、添加排除项来运行本工具；如发布物被拦截，应先核验 SHA-256、源码和构建来源。

## 参考研究

实现参考了 GitHub 上的同类防护项目，但没有复制病毒样本或高风险的一键执行逻辑。取舍记录见 [docs/REFERENCE_RESEARCH.md](docs/REFERENCE_RESEARCH.md)。

## 许可证

MIT。仅用于合法安全防护、应急响应和研究。
