#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进程扫描模块
Process Scanner Module
"""

import psutil
import os
from ioc import MaliciousProcesses

class ProcessScanner:
    """进程扫描器"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.malicious_processes = MaliciousProcesses()
        
        # 可疑进程特征
        self.suspicious_characteristics = {
            'suspicious_paths': [
                r"C:\Temp",
                r"C:\Windows\Temp",
                r"C:\Users\*\AppData\Local\Temp"
            ],
            'suspicious_parents': [
                "explorer.exe",
                "svchost.exe",
                "services.exe"
            ]
        }
    
    def scan(self):
        """扫描进程"""
        results = []
        
        # 获取所有进程
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'create_time']):
            try:
                # 检查进程是否可疑
                if self.is_suspicious_process(proc):
                    results.append({
                        'type': 'process',
                        'severity': 'high',
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'path': proc.info['exe'],
                        'cmdline': proc.info['cmdline'],
                        'detail': f'可疑进程: {proc.info["name"]}',
                        'action': 'recommend_terminate'
                    })
                
                # 检查进程是否是恶意进程
                elif self.is_malicious_process(proc):
                    results.append({
                        'type': 'process',
                        'severity': 'critical',
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'path': proc.info['exe'],
                        'cmdline': proc.info['cmdline'],
                        'detail': f'恶意进程: {proc.info["name"]}',
                        'action': 'recommend_terminate'
                    })
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        return results
    
    def is_suspicious_process(self, proc):
        """检查是否是可疑进程"""
        try:
            # 检查进程路径
            proc_path = proc.info['exe']
            if proc_path:
                for suspicious_path in self.suspicious_characteristics['suspicious_paths']:
                    if '*' in suspicious_path:
                        # 处理通配符路径
                        import glob
                        for expanded_path in glob.glob(suspicious_path):
                            if proc_path.startswith(expanded_path):
                                return True
                    else:
                        if proc_path.startswith(suspicious_path):
                            return True
            
            # 检查父进程
            try:
                parent = proc.parent()
                if parent and parent.name() in self.suspicious_characteristics['suspicious_parents']:
                    # 检查进程是否在可疑位置
                    if proc_path and any(suspicious in proc_path for suspicious in ['Temp', 'AppData']):
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            
            # 检查命令行参数
            cmdline = proc.info['cmdline']
            if cmdline:
                cmdline_str = ' '.join(cmdline).lower()
                suspicious_patterns = [
                    'powershell',
                    'cmd.exe',
                    'wscript',
                    'cscript',
                    'mshta',
                    'rundll32'
                ]
                for pattern in suspicious_patterns:
                    if pattern in cmdline_str:
                        return True
            
            return False
            
        except Exception as e:
            if self.verbose:
                print(f"检查进程时出错: {e}")
            return False
    
    def is_malicious_process(self, proc):
        """检查是否是恶意进程"""
        try:
            # 检查进程名称
            proc_name = proc.info['name']
            if proc_name in self.malicious_processes.get_process_names():
                return True
            
            # 检查进程路径
            proc_path = proc.info['exe']
            if proc_path:
                malicious_paths = self.malicious_processes.get_process_paths()
                for malicious_path in malicious_paths:
                    if proc_path.startswith(malicious_path):
                        return True
            
            return False
            
        except Exception as e:
            if self.verbose:
                print(f"检查进程时出错: {e}")
            return False
    
    def get_process_by_name(self, name):
        """根据名称获取进程"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            if proc.info['name'] == name:
                processes.append(proc)
        return processes
    
    def get_process_by_pid(self, pid):
        """根据PID获取进程"""
        try:
            return psutil.Process(pid)
        except psutil.NoSuchProcess:
            return None
    
    def is_process_running(self, name):
        """检查进程是否在运行"""
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == name:
                return True
        return False
