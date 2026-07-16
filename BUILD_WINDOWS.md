# Windows 构建说明

## 本地构建

要求 Windows 10/11、Python 3.10+，并建议从干净虚拟环境构建。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
.\build_windows.ps1 -Python .\.venv\Scripts\python.exe
```

脚本会依次安装 `requirements-dev.txt`、运行安全测试、构建两个单文件 EXE，并生成 `dist\SHA256SUMS.txt`。重复构建前请关闭已启动的 GUI，否则 Windows 会锁定旧 EXE。

输出：

- `dist\SilverFoxKiller.exe`
- `dist\SilverFoxKillerGUI.exe`
- `dist\SHA256SUMS.txt`

## GitHub Actions

`.github/workflows/build.yml` 支持：

- 手动触发 `workflow_dispatch`；
- 推送 `v*` 标签时自动构建并创建 Release；
- 发布 CLI、GUI 和 SHA-256 校验文件。

## 发布建议

正式分发前建议增加 Authenticode 代码签名，并在隔离的 Windows 10/11 虚拟机验证：普通用户扫描、管理员扫描、隔离/恢复、UAC、中文用户名和无网络环境。

PyInstaller 单文件程序可能触发启发式告警。不要建议用户关闭杀毒软件或添加排除项；应提供源码、可复现构建、哈希和代码签名来降低供应链风险。
