#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恶意注册表键数据库
Malicious Registry Keys Database - 银狐木马 IOC
"""

class MaliciousRegistryKeys:
    """恶意注册表键"""
    
    def __init__(self):
        # 银狐病毒已知的恶意注册表键
        self.registry_keys = {
            # ========== Run键持久化 ==========
            "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run": [
                "SilverFox",
                "WinUpdateService",
                "Microsoftdata",
            ],
            "HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run": [
                "SilverFox",
                "WinUpdateService",
                "Microsoftdata",
            ],
            
            
            # ========== 服务注册 ==========
            "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services": [
                "Zowieg951d475sbs",
                "SilverFoxService",
                "WinUpdateSvc",
                "WindowsDefenderSvc",
                "NetworkService",
                "SystemEventNotificationService",
            ],
            
            # ========== 计划任务持久化 ==========
            "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tree": [
                "\\Microsoft\\Windows\\Application Experience\\Microsoft Compatibility Appraiser",
                "\\Microsoft\\Windows\\Customer Experience Improvement Program\\Consolidator",
                "\\Microsoft\\Windows\\DiskDiagnostic\\Microsoft-Windows-DiskDiagnosticDataCollector",
                "\\Microsoft\\Windows\\PI\\Sqm-Tasks",
            ],
            
            # ========== ETW/AMSI绕过 ==========
            "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System": [
                "EnableLUA",
                "ConsentPromptBehaviorAdmin",
            ],
            
            # ========== WMI持久化 ==========
            "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\WBEM\\WDM": [
                "CommandLineEventConsumer",
            ],
            
            # ========== 注册表Shellcode存储 ==========
            "HKEY_CURRENT_USER\\Console": [
                "hrqnmlb",
            ],
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
    
    def search_key(self, query):
        """搜索注册表键值（支持部分匹配）"""
        query_lower = query.lower()
        results = {}
        for key_path, values in self.registry_keys.items():
            matching_values = [v for v in values if query_lower in v.lower()]
            if matching_values or query_lower in key_path.lower():
                results[key_path] = matching_values
        return results
