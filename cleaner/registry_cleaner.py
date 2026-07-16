#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
注册表清除模块
Registry Cleaner Module
"""

import sys
import time

# 检查是否在Windows系统上运行
if sys.platform == 'win32':
    import winreg
else:
    winreg = None

class RegistryCleaner:
    """注册表清除器"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def clean_registry(self, threat_info):
        """清除指定注册表项"""
        # 如果不是Windows系统，返回跳过结果
        if sys.platform != 'win32':
            return {
                'type': 'registry',
                'action': 'skipped',
                'detail': '注册表清除仅在Windows系统上支持',
                'success': False,
                'skipped': True
            }
        
        try:
            registry_path = threat_info.get('path')
            if not registry_path:
                return {
                    'type': 'registry',
                    'action': 'skipped',
                    'detail': '未指定注册表路径',
                    'success': False,
                    'skipped': True
                }
            
            # 解析注册表路径
            parts = registry_path.split('\\')
            if len(parts) < 2:
                return {
                    'type': 'registry',
                    'action': 'skipped',
                    'detail': f'无效的注册表路径: {registry_path}',
                    'success': False,
                    'skipped': True
                }
            
            # 获取注册表键和值名称
            key_path = '\\'.join(parts[:-1])
            value_name = parts[-1]
            
            # 确定注册表配置单元
            hive = self.get_hive_from_path(key_path)
            if not hive:
                return {
                    'type': 'registry',
                    'action': 'skipped',
                    'detail': f'无法确定注册表配置单元: {key_path}',
                    'success': False,
                    'skipped': True
                }
            
            # 删除注册表值
            if self.delete_registry_value(hive, key_path, value_name):
                return {
                    'type': 'registry',
                    'action': 'deleted',
                    'path': registry_path,
                    'detail': f'成功删除注册表项: {registry_path}',
                    'success': True
                }
            else:
                return {
                    'type': 'registry',
                    'action': 'failed',
                    'path': registry_path,
                    'detail': f'无法删除注册表项: {registry_path}',
                    'success': False
                }
                
        except Exception as e:
            if self.verbose:
                print(f"清除注册表时出错: {e}")
            return {
                'type': 'registry',
                'action': 'error',
                'detail': f'清除注册表时出错: {e}',
                'success': False
            }
    
    def delete_registry_value(self, hive, key_path, value_name):
        """删除注册表值"""
        try:
            # 打开注册表键
            key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_WRITE)
            
            # 删除值
            winreg.DeleteValue(key, value_name)
            
            # 关闭键
            winreg.CloseKey(key)
            
            return True
            
        except WindowsError as e:
            if self.verbose:
                print(f"删除注册表值时出错: {e}")
            return False
    
    def get_hive_from_path(self, key_path):
        """根据路径获取注册表配置单元"""
        if key_path.startswith("HKEY_CURRENT_USER"):
            return winreg.HKEY_CURRENT_USER
        elif key_path.startswith("HKEY_LOCAL_MACHINE"):
            return winreg.HKEY_LOCAL_MACHINE
        elif key_path.startswith("HKEY_CLASSES_ROOT"):
            return winreg.HKEY_CLASSES_ROOT
        elif key_path.startswith("HKEY_USERS"):
            return winreg.HKEY_USERS
        elif key_path.startswith("HKEY_CURRENT_CONFIG"):
            return winreg.HKEY_CURRENT_CONFIG
        else:
            return None
    
    def clean_registry_key(self, hive, key_path):
        """删除整个注册表键"""
        try:
            # 打开父键
            parent_path = '\\'.join(key_path.split('\\')[:-1])
            key_name = key_path.split('\\')[-1]
            
            parent_key = winreg.OpenKey(hive, parent_path, 0, winreg.KEY_WRITE)
            
            # 删除键
            winreg.DeleteKey(parent_key, key_name)
            
            # 关闭父键
            winreg.CloseKey(parent_key)
            
            return True
            
        except WindowsError as e:
            if self.verbose:
                print(f"删除注册表键时出错: {e}")
            return False
    
    def clean_all(self):
        """清除所有恶意注册表项"""
        results = []
        
        # 如果不是Windows系统，返回空结果
        if sys.platform != 'win32':
            if self.verbose:
                print("注册表清除仅在Windows系统上支持")
            return results
        
        # 常见恶意注册表路径
        malicious_registry_paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "SilverFox"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "WinUpdateService"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "SilverFox"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "WinUpdateService"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "AppInit_DLLs")
        ]
        
        for hive, key_path, value_name in malicious_registry_paths:
            if self.registry_value_exists(hive, key_path, value_name):
                result = self.clean_registry({
                    'path': f"{key_path}\\{value_name}"
                })
                results.append(result)
        
        return results
    
    def registry_value_exists(self, hive, key_path, value_name):
        """检查注册表值是否存在"""
        if sys.platform != 'win32':
            return False
        
        try:
            key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, value_name)
            winreg.CloseKey(key)
            return True
        except WindowsError:
            return False
    
    def backup_registry_key(self, hive, key_path, backup_file):
        """备份注册表键"""
        try:
            import subprocess
            result = subprocess.run(
                ['reg', 'export', f'{hive}\\{key_path}', backup_file],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            if self.verbose:
                print(f"备份注册表键时出错: {e}")
            return False
    
    def restore_registry_key(self, backup_file):
        """恢复注册表键"""
        try:
            import subprocess
            result = subprocess.run(
                ['reg', 'import', backup_file],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            if self.verbose:
                print(f"恢复注册表键时出错: {e}")
            return False
