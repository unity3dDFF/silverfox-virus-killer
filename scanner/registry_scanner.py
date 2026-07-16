#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
注册表扫描模块
Registry Scanner Module
"""

import sys
from ioc import MaliciousRegistryKeys

# 检查是否在Windows系统上运行
if sys.platform == 'win32':
    import winreg
else:
    winreg = None

class RegistryScanner:
    """注册表扫描器"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.malicious_keys = MaliciousRegistryKeys()
        
        # 常见恶意注册表路径
        if sys.platform == 'win32':
            self.registry_paths = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
            ]
        else:
            self.registry_paths = []
    
    def scan(self):
        """扫描注册表"""
        results = []
        
        # 如果不是Windows系统，返回空结果
        if sys.platform != 'win32':
            if self.verbose:
                print("注册表扫描仅在Windows系统上支持")
            return results
        
        for hive, path in self.registry_paths:
            try:
                results.extend(self.scan_registry_key(hive, path))
            except Exception as e:
                if self.verbose:
                    print(f"扫描注册表时出错 {path}: {e}")
        
        return results
    
    def scan_registry_key(self, hive, key_path):
        """扫描指定注册表键"""
        results = []
        
        try:
            # 打开注册表键
            key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ)
            
            # 枚举所有值
            i = 0
            while True:
                try:
                    name, value, type = winreg.EnumValue(key, i)
                    
                    # 检查是否是恶意值
                    if self.is_malicious_value(name, value):
                        results.append({
                            'type': 'registry',
                            'severity': 'high',
                            'path': f"{key_path}\\{name}",
                            'value': value,
                            'detail': f'恶意注册表项: {name}',
                            'action': 'recommend_delete'
                        })
                    
                    # 检查是否是可疑值
                    elif self.is_suspicious_value(name, value):
                        results.append({
                            'type': 'registry',
                            'severity': 'medium',
                            'path': f"{key_path}\\{name}",
                            'value': value,
                            'detail': f'可疑注册表项: {name}',
                            'action': 'recommend_investigate'
                        })
                    
                    i += 1
                except WindowsError:
                    break
            
            winreg.CloseKey(key)
            
        except Exception as e:
            if self.verbose:
                print(f"无法访问注册表键 {key_path}: {e}")
        
        return results
    
    def is_malicious_value(self, name, value):
        """检查是否是恶意注册表值"""
        # 检查恶意值名称
        malicious_names = self.malicious_keys.get_value_names()
        if name in malicious_names:
            return True
        
        # 检查恶意值内容
        malicious_values = self.malicious_keys.get_value_contents()
        for malicious_value in malicious_values:
            if malicious_value in value:
                return True
        
        return False
    
    def is_suspicious_value(self, name, value):
        """检查是否是可疑注册表值"""
        # 检查可疑模式
        suspicious_patterns = [
            "rundll32.exe",
            "mshta.exe",
            "wscript.exe",
            "cscript.exe",
            "powershell.exe",
            "cmd.exe"
        ]
        
        for pattern in suspicious_patterns:
            if pattern in value.lower():
                return True
        
        # 检查可疑路径
        suspicious_paths = [
            r"C:\Temp",
            r"C:\Windows\Temp",
            r"%TEMP%",
            r"%APPDATA%"
        ]
        
        for path in suspicious_paths:
            if path in value:
                return True
        
        return False
    
    def is_key_exists(self, hive, key_path):
        """检查注册表键是否存在"""
        try:
            winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ)
            return True
        except WindowsError:
            return False
    
    def get_value(self, hive, key_path, value_name):
        """获取注册表值"""
        try:
            key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ)
            value, type = winreg.QueryValueEx(key, value_name)
            winreg.CloseKey(key)
            return value
        except WindowsError:
            return None
