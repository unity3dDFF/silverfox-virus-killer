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
    
    def scan_all(self):
        """执行全面扫描"""
        results = []
        
        if self.verbose:
            print("[扫描] 开始文件扫描...")
        results.extend(self.file_scanner.scan())
        
        if self.verbose:
            print("[扫描] 开始注册表扫描...")
        results.extend(self.registry_scanner.scan())
        
        if self.verbose:
            print("[扫描] 开始进程扫描...")
        results.extend(self.process_scanner.scan())
        
        if self.verbose:
            print("[扫描] 开始网络连接扫描...")
        results.extend(self.network_scanner.scan())
        
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
