#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恶意进程数据库
Malicious Processes Database - 银狐木马 IOC
"""

class MaliciousProcesses:
    """恶意进程"""
    
    def __init__(self):
        # 银狐病毒已知的恶意进程
        self.malicious_processes = {
            # 恶意进程名称
            "names": [
                # ========== 2026年7月 - ValleyRAT ==========
                "GjdLUhqZIJJB.exe",
                
                # ========== 2026年3月 - 内核驱动对抗 ==========
                "KGseKKdKce.exe",
                "NtHandleCallback.exe",
                "main.exe",
                "bypass.exe",
                "NVIDIA.exe",
                "tree.exe",
                "kail.exe",
                
                # ========== 2026年1月 - 伪装Telegram ==========
                "OTGContainer.exe",
                "FFLOADER.exe",
                "Telegram.exe",
                "tracerpt.exe",
                
                # ========== 银狐通用恶意进程 ==========
                "银狐.exe",
                "silverfox.exe",
                "silver_fox.exe",
                "Microsoftdata.exe",
                "R2-Signed.exe",
                "SSRClient.exe",
                "updat4.vac",
                
            ],
            
            # 恶意进程路径
            "paths": [
                r"C:\Drivers",
                r"C:\Temp",
                r"C:\Windows\Temp",
                r"C:\Users\*\AppData\Local\Temp",
                r"C:\Users\Public\Documents",
                r"C:\Users\Public\Downloads",
                r"C:\ProgramData",
                r"C:\WhatsAppBackup",
            ],
            
            # 恶意进程命令行模式
            "cmdline_patterns": [
                "powershell",
                "cmd.exe",
                "wscript",
                "cscript",
                "mshta",
                "rundll32",
                "7zr.exe x -y -bd",
                "locale.dat",
                "locale2.dat",
                "locale7.dat",
                "Server8888",
                "htLcENyRFYwXsHFnUnqK",
                "?Bid@locale@std",
                "Windows Defender扫描例外",
                "Add-MpPreference",
                "Set-MpPreference",
                "bb.jpg",
                "bb2.jpg",
                "hrqnmlb",
            ],
            
            # 注入目标进程
            "injection_targets": [
                "svchost.exe",
                "explorer.exe",
                "tracerpt.exe",
                "notepad.exe",
            ],
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
    
    def get_injection_targets(self):
        """获取注入目标进程"""
        return self.malicious_processes.get("injection_targets", [])
    
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
    
    def search_process(self, query):
        """搜索进程名（支持部分匹配）"""
        query_lower = query.lower()
        return [p for p in self.malicious_processes["names"] if query_lower in p.lower()]
