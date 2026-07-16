# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for SilverFox Virus Killer GUI

block_cipher = None

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'scanner',
        'scanner.file_scanner',
        'scanner.registry_scanner',
        'scanner.process_scanner',
        'scanner.network_scanner',
        'cleaner',
        'cleaner.process_cleaner',
        'cleaner.file_cleaner',
        'cleaner.registry_cleaner',
        '修复',
        '修复.system_repair',
        'reports',
        'reports.report_generator',
        'ioc',
        'ioc.file_hashes',
        'ioc.domains',
        'ioc.files',
        'ioc.processes',
        'ioc.ips',
        'ioc.ports',
        'ioc.registry_keys',
        'utils',
        'utils.common',
        'psutil',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SilverFoxKillerGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SilverFoxKillerGUI',
)
