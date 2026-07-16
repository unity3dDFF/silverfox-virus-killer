#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统修复模块
System Repair Module
"""

from .system_repair import SystemRepair as _BaseSystemRepair

class SystemRepair(_BaseSystemRepair):
    """系统修复器（带repair_all方法）"""
    
    def repair_all(self):
        """修复所有系统设置"""
        results = []
        
        # 修复系统设置
        results.extend(self.repair_system_settings())
        
        # 修复安全设置
        results.extend(self.repair_security_settings())
        
        # 修复启动项
        results.extend(self.repair_startup_items())
        
        # 修复网络设置
        results.extend(self.repair_network_settings())
        
        return results
    
    def get_repair_summary(self, results):
        """获取修复摘要"""
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
