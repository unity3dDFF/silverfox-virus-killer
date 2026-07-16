#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件扫描模块
File Scanner Module
"""

import os
import hashlib
from pathlib import Path
from ioc import MaliciousFiles, MaliciousHashes

class FileScanner:
    """文件扫描器"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.malicious_files = MaliciousFiles()
        self.malicious_hashes = MaliciousHashes()
        
        # 常见恶意文件路径
        self.scan_paths = [
            r"C:\Program Files\Internet Explorer",
            r"C:\Users\Public\Documents",
            r"C:\Temp",
            r"C:\Windows\System32",
            r"C:\Users\*\AppData\Local\Temp",
            r"C:\Users\*\Downloads"
        ]
    
    def scan(self):
        """扫描文件系统"""
        results = []
        
        for path in self.scan_paths:
            if '*' in path:
                # 处理通配符路径
                import glob
                for expanded_path in glob.glob(path):
                    results.extend(self.scan_directory(expanded_path))
            else:
                if os.path.exists(path):
                    results.extend(self.scan_directory(path))
        
        return results
    
    def scan_directory(self, directory):
        """扫描指定目录"""
        results = []
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # 检查文件名
                    if self.is_malicious_filename(file):
                        results.append({
                            'type': 'file',
                            'severity': 'high',
                            'path': file_path,
                            'detail': f'可疑文件名: {file}',
                            'action': 'recommend_delete'
                        })
                    
                    # 检查文件哈希
                    file_hash = self.calculate_file_hash(file_path)
                    if file_hash and self.is_malicious_hash(file_hash):
                        results.append({
                            'type': 'file',
                            'severity': 'critical',
                            'path': file_path,
                            'detail': f'恶意文件哈希: {file_hash}',
                            'action': 'recommend_delete'
                        })
                    
                    # 检查文件扩展名
                    if file.endswith(('.dll', '.exe', '.msi')) and self.is_suspicious_location(file_path):
                        results.append({
                            'type': 'file',
                            'severity': 'medium',
                            'path': file_path,
                            'detail': f'可疑位置的可执行文件',
                            'action': 'recommend_investigate'
                        })
                        
        except Exception as e:
            if self.verbose:
                print(f"扫描目录时出错 {directory}: {e}")
        
        return results
    
    def is_malicious_filename(self, filename):
        """检查是否是恶意文件名"""
        malicious_patterns = [
            "开票-目录",
            "违规-告示",
            "违规-记录",
            "金稅",
            "违纪名单",
            "裁员名单",
            "补偿方案",
            "内部调查结果"
        ]
        
        for pattern in malicious_patterns:
            if pattern in filename:
                return True
        return False
    
    def calculate_file_hash(self, file_path):
        """计算文件哈希"""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return None
    
    def is_malicious_hash(self, file_hash):
        """检查是否是恶意文件哈希"""
        return file_hash in self.malicious_hashes.get_hashes()
    
    def is_suspicious_location(self, file_path):
        """检查是否在可疑位置"""
        suspicious_locations = [
            r"C:\Temp",
            r"C:\Windows\Temp",
            r"C:\Users\*\AppData\Local\Temp"
        ]
        
        for location in suspicious_locations:
            if file_path.startswith(location.replace('*', '')):
                return True
        return False
