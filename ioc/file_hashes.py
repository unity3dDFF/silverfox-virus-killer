#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恶意文件哈希数据库
Malicious File Hashes Database
"""

class MaliciousHashes:
    """恶意文件哈希"""
    
    def __init__(self):
        # 银狐病毒已知的恶意文件哈希
        self.hashes = [
            # 2024年新变种
            "34101194d27df8bc823e339d590e18f2",
            "B736A809E7A0F1603C97D43BBC7D2EA8A9CD080B",
            "A672825339ADBB5EEEF8176D161266D4E4A4A625",
            "E49938CB6C4CE0D73DB2B4A32018B1FF71A2D7F0",
            "9CAA4EC93CE1CD40BD5975645A110A4325310A3B",
            "D7F41D457C8358AF840B06914D1BC969EF7939D0",
            "48B2090FDCEA7D7C0EB1544EBCDAF911796A7F67",
            
            # 2025年变种
            "1234567890abcdef1234567890abcdef",  # 示例，需要实际替换
            "abcdef1234567890abcdef1234567890",  # 示例，需要实际替换
            
            # 更多哈希值...
        ]
    
    def get_hashes(self):
        """获取所有恶意文件哈希"""
        return self.hashes
    
    def add_hash(self, file_hash):
        """添加新的恶意文件哈希"""
        if file_hash not in self.hashes:
            self.hashes.append(file_hash)
    
    def remove_hash(self, file_hash):
        """移除恶意文件哈希"""
        if file_hash in self.hashes:
            self.hashes.remove(file_hash)
    
    def is_malicious(self, file_hash):
        """检查文件哈希是否是恶意的"""
        return file_hash in self.hashes
    
    def get_hash_count(self):
        """获取恶意文件哈希数量"""
        return len(self.hashes)
