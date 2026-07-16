#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本
Test Script
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    
    try:
        from scanner import SilverFoxScanner
        print("✓ scanner 模块导入成功")
    except ImportError as e:
        print(f"✗ scanner 模块导入失败: {e}")
        return False
    
    try:
        from cleaner import SilverFoxCleaner
        print("✓ cleaner 模块导入成功")
    except ImportError as e:
        print(f"✗ cleaner 模块导入失败: {e}")
        return False
    
    try:
        import importlib
        修复_module = importlib.import_module('repair')
        SystemRepair = 修复_module.SystemRepair
        print("✓ 修复 模块导入成功")
    except ImportError as e:
        print(f"✗ 修复 模块导入失败: {e}")
        return False
    
    try:
        from reports import ReportGenerator
        print("✓ reports 模块导入成功")
    except ImportError as e:
        print(f"✗ reports 模块导入失败: {e}")
        return False
    
    try:
        from ioc import IOCDatabase
        print("✓ ioc 模块导入成功")
    except ImportError as e:
        print(f"✗ ioc 模块导入失败: {e}")
        return False
    
    return True

def test_scanner():
    """测试扫描器"""
    print("\n测试扫描器...")
    
    try:
        from scanner import SilverFoxScanner
        
        scanner = SilverFoxScanner(verbose=True)
        print("✓ 扫描器创建成功")
        
        # 测试文件扫描器
        from scanner.file_scanner import FileScanner
        file_scanner = FileScanner(verbose=True)
        print("✓ 文件扫描器创建成功")
        
        # 测试注册表扫描器
        from scanner.registry_scanner import RegistryScanner
        registry_scanner = RegistryScanner(verbose=True)
        print("✓ 注册表扫描器创建成功")
        
        # 测试进程扫描器
        from scanner.process_scanner import ProcessScanner
        process_scanner = ProcessScanner(verbose=True)
        print("✓ 进程扫描器创建成功")
        
        # 测试网络扫描器
        from scanner.network_scanner import NetworkScanner
        network_scanner = NetworkScanner(verbose=True)
        print("✓ 网络扫描器创建成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 扫描器测试失败: {e}")
        return False

def test_cleaner():
    """测试清除器"""
    print("\n测试清除器...")
    
    try:
        from cleaner import SilverFoxCleaner
        
        cleaner = SilverFoxCleaner(verbose=True)
        print("✓ 清除器创建成功")
        
        # 测试进程清除器
        from cleaner.process_cleaner import ProcessCleaner
        process_cleaner = ProcessCleaner(verbose=True)
        print("✓ 进程清除器创建成功")
        
        # 测试文件清除器
        from cleaner.file_cleaner import FileCleaner
        file_cleaner = FileCleaner(verbose=True)
        print("✓ 文件清除器创建成功")
        
        # 测试注册表清除器
        from cleaner.registry_cleaner import RegistryCleaner
        registry_cleaner = RegistryCleaner(verbose=True)
        print("✓ 注册表清除器创建成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 清除器测试失败: {e}")
        return False

def test_ioc():
    """测试IOC数据库"""
    print("\n测试IOC数据库...")
    
    try:
        from ioc import IOCDatabase
        
        ioc_db = IOCDatabase()
        print("✓ IOC数据库创建成功")
        
        # 测试获取IOC
        all_iocs = ioc_db.get_all_iocs()
        print(f"✓ 获取IOC成功，包含 {len(all_iocs)} 类IOC")
        
        # 测试各个IOC模块
        from ioc.file_hashes import MaliciousHashes
        hashes = MaliciousHashes()
        print(f"✓ 文件哈希数据库: {hashes.get_hash_count()} 个哈希")
        
        from ioc.domains import MaliciousDomains
        domains = MaliciousDomains()
        print(f"✓ 域名数据库: {domains.get_domain_count()} 个域名")
        
        from ioc.registry_keys import MaliciousRegistryKeys
        registry_keys = MaliciousRegistryKeys()
        print(f"✓ 注册表键数据库: {registry_keys.get_key_count()} 个键")
        
        return True
        
    except Exception as e:
        print(f"✗ IOC数据库测试失败: {e}")
        return False

def test_reports():
    """测试报告生成器"""
    print("\n测试报告生成器...")
    
    try:
        from reports import ReportGenerator
        
        report_gen = ReportGenerator(verbose=True)
        print("✓ 报告生成器创建成功")
        
        # 测试生成扫描报告
        test_results = [
            {
                'type': 'file',
                'severity': 'high',
                'path': 'C:\\Test\\malware.exe',
                'detail': '测试恶意文件',
                'action': 'recommend_delete'
            }
        ]
        
        # 生成测试报告
        test_report_file = 'test_report.txt'
        success = report_gen.generate_report('scan', test_results, test_report_file)
        
        if success:
            print(f"✓ 测试报告生成成功: {test_report_file}")
            # 清理测试文件
            if os.path.exists(test_report_file):
                os.remove(test_report_file)
        else:
            print("✗ 测试报告生成失败")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ 报告生成器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("银狐病毒专杀工具 - 测试脚本")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_imports),
        ("扫描器", test_scanner),
        ("清除器", test_cleaner),
        ("IOC数据库", test_ioc),
        ("报告生成器", test_reports)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"运行测试: {test_name}")
        print('='*40)
        
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} 测试通过")
            else:
                failed += 1
                print(f"✗ {test_name} 测试失败")
        except Exception as e:
            failed += 1
            print(f"✗ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    print(f"总计: {passed + failed}")
    
    if failed == 0:
        print("\n✓ 所有测试通过！")
        return 0
    else:
        print(f"\n✗ 有 {failed} 个测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
