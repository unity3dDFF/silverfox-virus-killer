#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银狐病毒专杀工具 - 主程序入口
SilverFox Virus Killer - Main Entry Point
"""

import sys
import argparse
from scanner import SilverFoxScanner
from cleaner import SilverFoxCleaner
import importlib
修复_module = importlib.import_module('repair')
SystemRepair = 修复_module.SystemRepair
from reports import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description='银狐病毒专杀工具')
    parser.add_argument('action', choices=['scan', 'clean', 'repair', 'full'],
                       help='执行操作: scan=扫描, clean=清除, repair=修复, full=完整处理')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='显示详细信息')
    parser.add_argument('--output', '-o', type=str, default='report.txt',
                       help='报告输出文件')
    parser.add_argument('--auto-fix', '-a', action='store_true',
                       help='自动修复发现的问题')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("银狐病毒专杀工具 v1.0")
    print("=" * 60)
    
    if args.action == 'scan' or args.action == 'full':
        print("\n[扫描] 开始扫描系统...")
        scanner = SilverFoxScanner(verbose=args.verbose)
        scan_results = scanner.scan_all()
        print(f"扫描完成，发现 {len(scan_results)} 个威胁")
        
        if args.action == 'scan':
            report_gen = ReportGenerator()
            report_gen.generate_report('scan', scan_results, args.output)
            print(f"扫描报告已保存到: {args.output}")
            return
    
    if args.action == 'clean' or args.action == 'full':
        print("\n[清除] 开始清除银狐病毒...")
        cleaner = SilverFoxCleaner(verbose=args.verbose)
        clean_results = cleaner.clean_all(scan_results if 'scan_results' in locals() else None)
        print(f"清除完成，处理了 {len(clean_results)} 个项目")
        
        if args.action == 'clean':
            report_gen = ReportGenerator()
            report_gen.generate_report('clean', clean_results, args.output)
            print(f"清除报告已保存到: {args.output}")
            return
    
    if args.action == 'repair' or args.action == 'full':
        print("\n[修复] 开始修复系统设置...")
        repair = SystemRepair(verbose=args.verbose)
        repair_results = repair.repair_all()
        print(f"修复完成，处理了 {len(repair_results)} 个设置")
        
        if args.action == 'repair':
            report_gen = ReportGenerator()
            report_gen.generate_report('repair', repair_results, args.output)
            print(f"修复报告已保存到: {args.output}")
            return
    
    if args.action == 'full':
        print("\n[完成] 银狐病毒处理完成！")
        report_gen = ReportGenerator()
        report_gen.generate_full_report(
            scan_results if 'scan_results' in locals() else [],
            clean_results if 'clean_results' in locals() else [],
            repair_results if 'repair_results' in locals() else [],
            args.output
        )
        print(f"完整报告已保存到: {args.output}")

if __name__ == "__main__":
    main()
