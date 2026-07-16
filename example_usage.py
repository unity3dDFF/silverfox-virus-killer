#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用示例
Example Usage
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def example_scan():
    """扫描示例"""
    print("=" * 60)
    print("扫描示例")
    print("=" * 60)
    
    from scanner import SilverFoxScanner
    
    # 创建扫描器
    scanner = SilverFoxScanner(verbose=True)
    
    # 执行扫描
    print("开始扫描系统...")
    results = scanner.scan_all()
    
    # 显示结果
    print(f"\n扫描完成，发现 {len(results)} 个威胁")
    
    if results:
        print("\n威胁详情:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.get('detail', '未知威胁')}")
            print(f"   类型: {result.get('type', 'unknown')}")
            print(f"   严重性: {result.get('severity', 'unknown')}")
            print(f"   路径: {result.get('path', 'N/A')}")
            print()
    
    return results

def example_clean(scan_results=None):
    """清除示例"""
    print("=" * 60)
    print("清除示例")
    print("=" * 60)
    
    from cleaner import SilverFoxCleaner
    
    # 创建清除器
    cleaner = SilverFoxCleaner(verbose=True)
    
    # 执行清除
    print("开始清除病毒...")
    results = cleaner.clean_all(scan_results)
    
    # 显示结果
    print(f"\n清除完成，处理了 {len(results)} 个项目")
    
    if results:
        print("\n清除详情:")
        for i, result in enumerate(results, 1):
            status = "✓" if result.get('success', False) else "✗"
            print(f"{i}. {status} {result.get('detail', '未知操作')}")
            print(f"   类型: {result.get('type', 'unknown')}")
            print(f"   操作: {result.get('action', 'unknown')}")
            print()
    
    return results

def example_repair():
    """修复示例"""
    print("=" * 60)
    print("修复示例")
    print("=" * 60)
    
    import importlib
    修复_module = importlib.import_module('修复')
    SystemRepair = 修复_module.SystemRepair
    
    # 创建修复器
    repair = SystemRepair(verbose=True)
    
    # 执行修复
    print("开始修复系统...")
    results = repair.repair_all()
    
    # 显示结果
    print(f"\n修复完成，处理了 {len(results)} 个设置")
    
    if results:
        print("\n修复详情:")
        for i, result in enumerate(results, 1):
            status = "✓" if result.get('success', False) else "✗"
            print(f"{i}. {status} {result.get('detail', '未知操作')}")
            print(f"   类型: {result.get('type', 'unknown')}")
            print(f"   操作: {result.get('action', 'unknown')}")
            print()
    
    return results

def example_report(scan_results, clean_results, repair_results):
    """报告示例"""
    print("=" * 60)
    print("报告示例")
    print("=" * 60)
    
    from reports import ReportGenerator
    
    # 创建报告生成器
    report_gen = ReportGenerator(verbose=True)
    
    # 生成完整报告
    output_file = "example_report.txt"
    print(f"生成报告: {output_file}")
    
    success = report_gen.generate_full_report(
        scan_results,
        clean_results,
        repair_results,
        output_file
    )
    
    if success:
        print(f"✓ 报告生成成功: {output_file}")
        
        # 显示报告内容
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print("\n报告内容:")
        print(content)
        
        # 清理文件
        os.remove(output_file)
    else:
        print("✗ 报告生成失败")

def main():
    """主函数"""
    print("银狐病毒专杀工具 - 使用示例")
    print("=" * 60)
    
    try:
        # 1. 扫描示例
        scan_results = example_scan()
        
        # 2. 清除示例
        clean_results = example_clean(scan_results)
        
        # 3. 修复示例
        repair_results = example_repair()
        
        # 4. 报告示例
        example_report(scan_results, clean_results, repair_results)
        
        print("\n" + "=" * 60)
        print("示例执行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"执行示例时出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
