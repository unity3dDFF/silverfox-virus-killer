#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恶意注册表键数据库
Malicious Registry Keys Database
"""

class MaliciousRegistryKeys:
    """恶意注册表键"""
    
    def __init__(self):
        # 银狐病毒已知的恶意注册表键
        self.registry_keys = {
            # Run键持久化
            "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run": [
                "SilverFox",
                "WinUpdateService",
                "WindowsUpdate"
            ],
            "HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run": [
                "SilverFox",
                "WinUpdateService",
                "WindowsUpdate"
            ],
            
            # AppInit_DLLs
            "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Windows": [
                "AppInit_DLLs"
            ],
            
            # 更多注册表键...
        }
    
    def get_all_keys(self):
        """获取所有恶意注册表键"""
        return self.registry_keys
    
    def get_key_values(self, key_path):
        """获取指定键的恶意值"""
        return self.registry_keys.get(key_path, [])
    
    def add_key_value(self, key_path, value_name):
        """添加新的恶意注册表键值"""
        if key_path not in self.registry_keys:
            self.registry_keys[key_path] = []
        
        if value_name not in self.registry_keys[key_path]:
            self.registry_keys[key_path].append(value_name)
    
    def remove_key_value(self, key_path, value_name):
        """移除恶意注册表键值"""
        if key_path in self.registry_keys:
            if value_name in self.registry_keys[key_path]:
                self.registry_keys[key_path].remove(value_name)
    
    def is_malicious(self, key_path, value_name):
        """检查注册表键值是否是恶意的"""
        if key_path in self.registry_keys:
            return value_name in self.registry_keys[key_path]
        return False
    
    def get_key_count(self):
        """获取恶意注册表键数量"""
        return len(self.registry_keys)
    
    def get_value_count(self):
        """获取恶意注册表键值总数"""
        total = 0
        for values in self.registry_keys.values():
            total += len(values)
        return total
    
    def get_value_names(self):
        """获取所有恶意值名称"""
        value_names = []
        for values in self.registry_keys.values():
            value_names.extend(values)
        return value_names
    
    def get_value_contents(self):
        """获取所有恶意值内容"""
        # 这里可以添加恶意值内容的检测逻辑
        return []
