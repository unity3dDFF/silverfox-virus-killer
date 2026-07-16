#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银狐病毒清除模块
SilverFox Virus Cleaner Module
"""

from .process_cleaner import ProcessCleaner
from .file_cleaner import FileCleaner
from .registry_cleaner import RegistryCleaner

class SilverFoxCleaner:
    """银狐病毒清除器"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.process_cleaner = ProcessCleaner(verbose)
        self.file_cleaner = FileCleaner(verbose)
        self.registry_cleaner = RegistryCleaner(verbose)
    
    def clean_all(self, scan_results=None, progress_callback=None):
        """清除所有威胁"""
        results = []
        
        if scan_results:
            # 根据扫描结果进行清除
            total = len(scan_results)
            for index, result in enumerate(scan_results, 1):
                threat_type = result.get('type', '')
                
                if threat_type == 'process':
                    clean_result = self.process_cleaner.clean_process(result)
                    if clean_result:
                        results.append(clean_result)
                
                elif threat_type == 'file':
                    clean_result = self.file_cleaner.clean_file(result)
                    if clean_result:
                        results.append(clean_result)
                
                elif threat_type == 'registry':
                    clean_result = self.registry_cleaner.clean_registry(result)
                    if clean_result:
                        results.append(clean_result)
                
                elif threat_type == 'network':
                    # 本工具不伪装已执行防火墙操作；网络项留给人工复核。
                    results.append({
                        'type': 'network',
                        'action': 'skipped',
                        'detail': '网络连接仅报告，未自动添加防火墙规则',
                        'success': False,
                        'skipped': True
                    })
                if progress_callback:
                    progress_callback(index, total, result.get('detail', '正在处置'))
        else:
            results.append({
                'type': 'cleaner', 'action': 'skipped',
                'detail': '拒绝盲目清理：请先运行扫描并传入扫描结果',
                'success': False, 'skipped': True
            })
        
        return results
    
    def get_clean_summary(self, results):
        """获取清除摘要"""
        summary = {
            'total': len(results),
            'success': 0,
            'failed': 0,
            'skipped': 0
        }
        
        for result in results:
            if result.get('success', False):
                summary['success'] += 1
            elif result.get('skipped', False):
                summary['skipped'] += 1
            else:
                summary['failed'] += 1
        
        return summary
