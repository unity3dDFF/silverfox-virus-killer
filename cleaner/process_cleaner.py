#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进程清除模块
Process Cleaner Module
"""

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

import time

class ProcessCleaner:
    """进程清除器"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def clean_process(self, threat_info):
        """清除指定进程"""
        if not PSUTIL_AVAILABLE:
            if self.verbose:
                print("[警告] psutil未安装，无法清除进程")
            return {
                'type': 'process',
                'action': 'skipped',
                'detail': 'psutil未安装，无法清除进程',
                'success': False,
                'skipped': True
            }
        
        try:
            pid = threat_info.get('pid')
            if not pid:
                return {
                    'type': 'process',
                    'action': 'skipped',
                    'detail': '未指定PID',
                    'success': False,
                    'skipped': True
                }
            
            # 获取进程信息
            try:
                proc = psutil.Process(pid)
                proc_name = proc.name()
                proc_path = proc.exe()
            except psutil.NoSuchProcess:
                return {
                    'type': 'process',
                    'action': 'skipped',
                    'detail': f'进程 {pid} 不存在',
                    'success': False,
                    'skipped': True
                }
            
            # 尝试终止进程
            if self.terminate_process(proc):
                return {
                    'type': 'process',
                    'action': 'terminated',
                    'pid': pid,
                    'name': proc_name,
                    'path': proc_path,
                    'detail': f'成功终止进程: {proc_name} (PID: {pid})',
                    'success': True
                }
            else:
                return {
                    'type': 'process',
                    'action': 'failed',
                    'pid': pid,
                    'name': proc_name,
                    'path': proc_path,
                    'detail': f'无法终止进程: {proc_name} (PID: {pid})',
                    'success': False
                }
                
        except Exception as e:
            if self.verbose:
                print(f"清除进程时出错: {e}")
            return {
                'type': 'process',
                'action': 'error',
                'detail': f'清除进程时出错: {e}',
                'success': False
            }
    
    def terminate_process(self, proc):
        """终止进程"""
        if not PSUTIL_AVAILABLE:
            return False
        
        try:
            # 首先尝试正常终止
            proc.terminate()
            
            # 等待进程终止
            try:
                proc.wait(timeout=5)
                return True
            except psutil.TimeoutExpired:
                # 如果进程没有终止，强制终止
                if self.verbose:
                    print(f"进程 {proc.name()} 未在5秒内终止，尝试强制终止...")
                proc.kill()
                
                try:
                    proc.wait(timeout=5)
                    return True
                except psutil.TimeoutExpired:
                    if self.verbose:
                        print(f"无法强制终止进程 {proc.name()}")
                    return False
                    
        except psutil.AccessDenied:
            if self.verbose:
                print(f"没有权限终止进程 {proc.name()}")
            return False
        except Exception as e:
            if self.verbose:
                print(f"终止进程时出错: {e}")
            return False
    
    def clean_all(self):
        """清除所有可疑进程"""
        results = []
        
        if not PSUTIL_AVAILABLE:
            if self.verbose:
                print("[警告] psutil未安装，无法清除进程")
            return results
        
        # 获取所有进程
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                # 检查进程是否可疑
                if self.is_suspicious_process(proc):
                    result = self.clean_process({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'path': proc.info['exe']
                    })
                    results.append(result)
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        return results
    
    def is_suspicious_process(self, proc):
        """检查是否是可疑进程"""
        try:
            proc_name = proc.info['name']
            proc_path = proc.info['exe']
            
            # 检查进程名称
            suspicious_names = ['银狐', 'silverfox', 'silver_fox']
            for name in suspicious_names:
                if name in proc_name.lower():
                    return True
            
            # 检查进程路径
            if proc_path:
                suspicious_paths = ['Temp', 'AppData', 'Downloads']
                for path in suspicious_paths:
                    if path in proc_path:
                        return True
            
            return False
            
        except Exception:
            return False
    
    def terminate_process_by_name(self, name):
        """根据名称终止进程"""
        results = []
        
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == name:
                result = self.clean_process({
                    'pid': proc.info['pid'],
                    'name': proc.info['name']
                })
                results.append(result)
        
        return results
    
    def terminate_process_by_path(self, path):
        """根据路径终止进程"""
        results = []
        
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            if proc.info['exe'] and proc.info['exe'].startswith(path):
                result = self.clean_process({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'path': proc.info['exe']
                })
                results.append(result)
        
        return results
