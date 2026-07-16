#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成器
Report Generator
"""

import datetime
import json

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def generate_report(self, report_type, results, output_file):
        """生成报告"""
        try:
            # 生成报告内容
            if report_type == 'scan':
                content = self.generate_scan_report_content(results)
            elif report_type == 'clean':
                content = self.generate_clean_report_content(results)
            elif report_type == 'repair':
                content = self.generate_repair_report_content(results)
            else:
                content = self.generate_default_report_content(results)
            
            # 写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if self.verbose:
                print(f"报告已生成: {output_file}")
            
            return True
            
        except Exception as e:
            if self.verbose:
                print(f"生成报告时出错: {e}")
            return False
    
    def generate_full_report(self, scan_results, clean_results, repair_results, output_file):
        """生成完整报告"""
        try:
            content = self.generate_full_report_content(scan_results, clean_results, repair_results)
            
            # 写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if self.verbose:
                print(f"完整报告已生成: {output_file}")
            
            return True
            
        except Exception as e:
            if self.verbose:
                print(f"生成完整报告时出错: {e}")
            return False
    
    def generate_scan_report_content(self, results):
        """生成扫描报告内容"""
        report = []
        report.append("=" * 60)
        report.append("银狐病毒扫描报告")
        report.append("=" * 60)
        report.append(f"生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"扫描结果: 发现 {len(results)} 个威胁")
        report.append("")
        
        # 按类型分组
        threats_by_type = {}
        for result in results:
            threat_type = result.get('type', 'unknown')
            if threat_type not in threats_by_type:
                threats_by_type[threat_type] = []
            threats_by_type[threat_type].append(result)
        
        # 生成各类型报告
        for threat_type, threats in threats_by_type.items():
            report.append(f"【{threat_type.upper()}威胁】 ({len(threats)} 个)")
            report.append("-" * 40)
            
            for i, threat in enumerate(threats, 1):
                report.append(f"{i}. {threat.get('detail', '未知威胁')}")
                report.append(f"   路径: {threat.get('path', 'N/A')}")
                report.append(f"   严重性: {threat.get('severity', 'unknown')}")
                report.append(f"   建议操作: {threat.get('action', 'unknown')}")
                report.append("")
        
        report.append("=" * 60)
        report.append("扫描完成")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def generate_clean_report_content(self, results):
        """生成清除报告内容"""
        report = []
        report.append("=" * 60)
        report.append("银狐病毒清除报告")
        report.append("=" * 60)
        report.append(f"生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"清除结果: 处理了 {len(results)} 个项目")
        report.append("")
        
        # 统计结果
        success_count = sum(1 for r in results if r.get('success', False))
        failed_count = sum(1 for r in results if not r.get('success', False))
        
        report.append(f"成功: {success_count} 个")
        report.append(f"失败: {failed_count} 个")
        report.append("")
        
        # 详细结果
        report.append("详细结果:")
        report.append("-" * 40)
        
        for i, result in enumerate(results, 1):
            status = "✓" if result.get('success', False) else "✗"
            report.append(f"{i}. {status} {result.get('detail', '未知操作')}")
            report.append(f"   类型: {result.get('type', 'unknown')}")
            report.append(f"   操作: {result.get('action', 'unknown')}")
            report.append("")
        
        report.append("=" * 60)
        report.append("清除完成")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def generate_repair_report_content(self, results):
        """生成修复报告内容"""
        report = []
        report.append("=" * 60)
        report.append("系统修复报告")
        report.append("=" * 60)
        report.append(f"生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"修复结果: 处理了 {len(results)} 个设置")
        report.append("")
        
        # 统计结果
        success_count = sum(1 for r in results if r.get('success', False))
        failed_count = sum(1 for r in results if not r.get('success', False))
        
        report.append(f"成功: {success_count} 个")
        report.append(f"失败: {failed_count} 个")
        report.append("")
        
        # 详细结果
        report.append("详细结果:")
        report.append("-" * 40)
        
        for i, result in enumerate(results, 1):
            status = "✓" if result.get('success', False) else "✗"
            report.append(f"{i}. {status} {result.get('detail', '未知操作')}")
            report.append(f"   类型: {result.get('type', 'unknown')}")
            report.append(f"   操作: {result.get('action', 'unknown')}")
            report.append("")
        
        report.append("=" * 60)
        report.append("修复完成")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def generate_full_report_content(self, scan_results, clean_results, repair_results):
        """生成完整报告内容"""
        report = []
        report.append("=" * 60)
        report.append("银狐病毒处理完整报告")
        report.append("=" * 60)
        report.append(f"生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # 扫描结果摘要
        report.append("【扫描结果摘要】")
        report.append("-" * 40)
        report.append(f"发现威胁: {len(scan_results)} 个")
        
        # 按类型统计
        threat_types = {}
        for result in scan_results:
            threat_type = result.get('type', 'unknown')
            threat_types[threat_type] = threat_types.get(threat_type, 0) + 1
        
        for threat_type, count in threat_types.items():
            report.append(f"  {threat_type}: {count} 个")
        
        report.append("")
        
        # 清除结果摘要
        report.append("【清除结果摘要】")
        report.append("-" * 40)
        clean_success = sum(1 for r in clean_results if r.get('success', False))
        clean_failed = sum(1 for r in clean_results if not r.get('success', False))
        report.append(f"处理项目: {len(clean_results)} 个")
        report.append(f"成功: {clean_success} 个")
        report.append(f"失败: {clean_failed} 个")
        report.append("")
        
        # 修复结果摘要
        report.append("【修复结果摘要】")
        report.append("-" * 40)
        repair_success = sum(1 for r in repair_results if r.get('success', False))
        repair_failed = sum(1 for r in repair_results if not r.get('success', False))
        report.append(f"处理设置: {len(repair_results)} 个")
        report.append(f"成功: {repair_success} 个")
        report.append(f"失败: {repair_failed} 个")
        report.append("")
        
        # 总结
        report.append("【总结】")
        report.append("-" * 40)
        
        total_success = clean_success + repair_success
        total_failed = clean_failed + repair_failed
        
        if total_failed == 0:
            report.append("所有操作均已完成，系统已成功修复。")
        else:
            report.append(f"有 {total_failed} 个操作未成功，建议人工检查。")
        
        report.append("")
        report.append("=" * 60)
        report.append("报告生成完成")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def generate_default_report_content(self, results):
        """生成默认报告内容"""
        report = []
        report.append("=" * 60)
        report.append("银狐病毒处理报告")
        report.append("=" * 60)
        report.append(f"生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"处理结果: {len(results)} 个项目")
        report.append("")
        
        for i, result in enumerate(results, 1):
            report.append(f"{i}. {result.get('detail', '未知操作')}")
        
        report.append("=" * 60)
        report.append("处理完成")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def save_report_as_json(self, results, output_file):
        """保存报告为JSON格式"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            if self.verbose:
                print(f"JSON报告已生成: {output_file}")
            
            return True
            
        except Exception as e:
            if self.verbose:
                print(f"生成JSON报告时出错: {e}")
            return False
    
    def load_report_from_json(self, input_file):
        """从JSON文件加载报告"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                return json.load(f)
            
        except Exception as e:
            if self.verbose:
                print(f"加载JSON报告时出错: {e}")
            return None
