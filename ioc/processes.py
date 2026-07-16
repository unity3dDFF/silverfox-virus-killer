#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恶意进程数据库
Malicious Processes Database
"""

class MaliciousProcesses:
    """恶意进程"""
    
    def __init__(self):
        # 银狐病毒已知的恶意进程
        self.malicious_processes = {
            # 恶意进程名称
            "names": [
                "银狐.exe",
                "silverfox.exe",
                "silver_fox.exe",
                "svchost.exe",  # 注意：这个需要特别处理，因为系统也有这个进程
                "explorer.exe",  # 注意：这个需要特别处理，因为系统也有这个进程
                "notepad.exe"  # 注意：这个需要特别处理，因为系统也有这个进程
            ],
            
            # 恶意进程路径
            "paths": [
                r"C:\Temp",
                r"C:\Windows\Temp",
                r"C:\Users\*\AppData\Local\Temp",
                r"C:\Users\Public\Documents"
            ],
            
            # 恶意进程命令行模式
            "cmdline_patterns": [
                "powershell",
                "cmd.exe",
                "wscript",
                "cscript",
                "mshta",
                "rundll32"
            ]
        }
    
    def get_all_processes(self):
        """获取所有恶意进程信息"""
        return self.malicious_processes
    
    def get_process_names(self):
        """获取恶意进程名称"""
        return self.malicious_processes.get("names", [])
    
    def get_process_paths(self):
        """获取恶意进程路径"""
        return self.malicious_processes.get("paths", [])
    
    def get_cmdline_patterns(self):
        """获取恶意进程命令行模式"""
        return self.malicious_processes.get("cmdline_patterns", [])
    
    def add_process_name(self, name):
        """添加新的恶意进程名称"""
        if name not in self.malicious_processes["names"]:
            self.malicious_processes["names"].append(name)
    
    def add_process_path(self, path):
        """添加新的恶意进程路径"""
        if path not in self.malicious_processes["paths"]:
            self.malicious_processes["paths"].append(path)
    
    def add_cmdline_pattern(self, pattern):
        """添加新的恶意进程命令行模式"""
        if pattern not in self.malicious_processes["cmdline_patterns"]:
            self.malicious_processes["cmdline_patterns"].append(pattern)
    
    def is_malicious_name(self, process_name):
        """检查进程名称是否是恶意的"""
        return process_name in self.malicious_processes["names"]
    
    def is_malicious_path(self, process_path):
        """检查进程路径是否是恶意的"""
        for path in self.malicious_processes["paths"]:
            if '*' in path:
                # 处理通配符路径
                import glob
                for expanded_path in glob.glob(path):
                    if process_path.startswith(expanded_path):
                        return True
            else:
                if process_path.startswith(path):
                    return True
        return False
    
    def is_malicious_cmdline(self, cmdline):
        """检查进程命令行是否是恶意的"""
        cmdline_lower = cmdline.lower()
        for pattern in self.malicious_processes["cmdline_patterns"]:
            if pattern in cmdline_lower:
                return True
        return False
    
    def get_process_count(self):
        """获取恶意进程数量"""
        return len(self.malicious_processes["names"])
