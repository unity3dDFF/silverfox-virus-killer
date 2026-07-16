#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用工具函数
Common Utility Functions
"""

import os
import sys
import hashlib
import datetime

class CommonUtils:
    """通用工具类"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def calculate_file_hash(self, file_path):
        """计算文件哈希"""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            if self.verbose:
                print(f"计算文件哈希时出错: {e}")
            return None
    
    def calculate_md5(self, file_path):
        """计算文件MD5"""
        try:
            md5_hash = hashlib.md5()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    md5_hash.update(byte_block)
            return md5_hash.hexdigest()
        except Exception as e:
            if self.verbose:
                print(f"计算文件MD5时出错: {e}")
            return None
    
    def get_file_size(self, file_path):
        """获取文件大小"""
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            if self.verbose:
                print(f"获取文件大小时出错: {e}")
            return None
    
    def get_file_creation_time(self, file_path):
        """获取文件创建时间"""
        try:
            return datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        except Exception as e:
            if self.verbose:
                print(f"获取文件创建时间时出错: {e}")
            return None
    
    def get_file_modification_time(self, file_path):
        """获取文件修改时间"""
        try:
            return datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        except Exception as e:
            if self.verbose:
                print(f"获取文件修改时间时出错: {e}")
            return None
    
    def is_file_accessible(self, file_path):
        """检查文件是否可访问"""
        try:
            return os.access(file_path, os.R_OK)
        except Exception:
            return False
    
    def backup_file(self, file_path):
        """备份文件"""
        try:
            backup_path = f"{file_path}.backup.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            import shutil
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            if self.verbose:
                print(f"备份文件时出错: {e}")
            return None
    
    def create_directory(self, dir_path):
        """创建目录"""
        try:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            return True
        except Exception as e:
            if self.verbose:
                print(f"创建目录时出错: {e}")
            return False
    
    def get_system_info(self):
        """获取系统信息"""
        info = {
            'platform': sys.platform,
            'python_version': sys.version,
            'current_directory': os.getcwd(),
            'current_user': os.getlogin() if hasattr(os, 'getlogin') else 'unknown'
        }
        return info
    
    def format_size(self, size):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    
    def format_datetime(self, dt):
        """格式化日期时间"""
        if isinstance(dt, datetime.datetime):
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        return str(dt)
    
    def log_message(self, message, level='info'):
        """记录日志消息"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level.upper()}] {message}"
        
        if self.verbose:
            print(log_entry)
        
        return log_entry
    
    def safe_remove(self, file_path):
        """安全删除文件"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            if self.verbose:
                print(f"安全删除文件时出错: {e}")
            return False
    
    def safe_remove_directory(self, dir_path):
        """安全删除目录"""
        try:
            if os.path.exists(dir_path):
                import shutil
                shutil.rmtree(dir_path)
                return True
            return False
        except Exception as e:
            if self.verbose:
                print(f"安全删除目录时出错: {e}")
            return False
