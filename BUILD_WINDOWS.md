# 银狐病毒专杀工具 - Windows打包说明

## 快速打包（推荐）

### 方法1：使用批处理脚本（最简单）

1. 确保已安装 Python 3.8+
2. 双击运行 `build_windows.bat`
3. 等待打包完成
4. 在 `dist` 目录下找到生成的exe文件

### 方法2：手动打包

```bash
# 1. 安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 2. 打包CLI版本
pyinstaller --onefile --name SilverFoxKiller main.py

# 3. 打包GUI版本
pyinstaller --onefile --windowed --name SilverFoxKillerGUI gui.py
```

## 输出文件

打包完成后，在 `dist` 目录下会生成：

- `SilverFoxKiller.exe` - 命令行版本（需要在命令行中运行）
- `SilverFoxKillerGUI.exe` - 图形界面版本（双击即可运行）

## 使用方法

### 图形界面版本（推荐）

1. 双击 `SilverFoxKillerGUI.exe`
2. 点击"扫描系统"按钮
3. 查看扫描结果
4. 点击"清除病毒"按钮
5. 点击"修复系统"按钮

### 命令行版本

```bash
# 扫描系统
SilverFoxKiller.exe scan

# 清除病毒
SilverFoxKiller.exe clean

# 修复系统
SilverFoxKiller.exe repair

# 完整处理（扫描+清除+修复）
SilverFoxKiller.exe full
```

## 注意事项

1. **管理员权限**：某些操作需要管理员权限，右键exe选择"以管理员身份运行"
2. **杀毒软件**：打包后的exe可能会被杀毒软件误报，请添加信任
3. **Windows Defender**：如果被拦截，请在Windows Defender中添加排除项
4. **文件大小**：打包后的exe约10-15MB

## 常见问题

### Q: 打包失败怎么办？

A: 确保已安装Python 3.8+和pip，然后运行：
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
```

### Q: exe被杀毒软件删除怎么办？

A: 这是误报，请在杀毒软件中添加信任或排除项。

### Q: 运行时报错"缺少DLL"怎么办？

A: 尝试安装Visual C++ Redistributable：
https://aka.ms/vs/17/release/vc_redist.x64.exe

### Q: 如何创建便携版？

A: 使用 `--onefile` 参数会生成单个exe文件，可以直接复制使用。

## 技术说明

- 使用 PyInstaller 打包
- 支持 Python 3.8+
- 依赖 psutil 库
- GUI使用tkinter（Python内置）

## 免责声明

本工具仅供安全研究和防护使用。使用本工具所造成的任何后果，开发者不承担责任。
