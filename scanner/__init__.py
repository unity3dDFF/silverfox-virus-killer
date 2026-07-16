#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银狐病毒扫描模块
SilverFox Virus Scanner Module
"""

from .file_scanner import FileScanner
from .registry_scanner import RegistryScanner
from .process_scanner import ProcessScanner
from .network_scanner import NetworkScanner

class SilverFoxScanner:
    """银狐病毒扫描器"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.file_scanner = FileScanner(verbose)
        self.registry_scanner = RegistryScanner(verbose)
        self.process_scanner = ProcessScanner(verbose)
        self.network_scanner = NetworkScanner(verbose)
    
    def scan_all(self, progress_callback=None):
        """执行全面扫描"""
        results = []

        def progress(percent, message):
            if progress_callback:
                progress_callback(max(0, min(100, int(percent))), message)
        
        if self.verbose:
            print("[扫描] 开始文件扫描...")
        progress(0, "正在枚举候选文件…")
        results.extend(self.file_scanner.scan(
            lambda current, total, message: progress(
                5 + (current / max(total, 1)) * 65, message
            )
        ))
        
        if self.verbose:
            print("[扫描] 开始注册表扫描...")
        progress(72, "正在检查注册表启动项…")
        results.extend(self.registry_scanner.scan())
        
        if self.verbose:
            print("[扫描] 开始进程扫描...")
        progress(82, "正在校验运行进程…")
        results.extend(self.process_scanner.scan())
        
        if self.verbose:
            print("[扫描] 开始网络连接扫描...")
        progress(94, "正在检查活动网络连接…")
        results.extend(self.network_scanner.scan())
        progress(100, "扫描完成")
        
        return results
    
    def get_threat_count(self, results):
        """获取威胁数量"""
        return len(results)
    
    def get_threat_summary(self, results):
        """获取威胁摘要"""
        summary = {
            'files': 0,
            'registry': 0,
            'processes': 0,
            'network': 0
        }
        
        for result in results:
            threat_type = result.get('type', '')
            if threat_type == 'file':
                summary['files'] += 1
            elif threat_type == 'registry':
                summary['registry'] += 1
            elif threat_type == 'process':
                summary['processes'] += 1
            elif threat_type == 'network':
                summary['network'] += 1
        
        return summary
