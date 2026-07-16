#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件清除模块
File Cleaner Module
"""

import os
import shutil
import time

class FileCleaner:
    """文件清除器"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def clean_file(self, threat_info):
        """清除指定文件"""
        try:
            file_path = threat_info.get('path')
            if not file_path:
                return {
                    'type': 'file',
                    'action': 'skipped',
                    'detail': '未指定文件路径',
                    'success': False,
                    'skipped': True
                }
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return {
                    'type': 'file',
                    'action': 'skipped',
                    'detail': f'文件不存在: {file_path}',
                    'success': False,
                    'skipped': True
                }
            
            # 尝试删除文件
            if self.delete_file(file_path):
                return {
                    'type': 'file',
                    'action': 'deleted',
                    'path': file_path,
                    'detail': f'成功删除文件: {file_path}',
                    'success': True
                }
            else:
                return {
                    'type': 'file',
                    'action': 'failed',
                    'path': file_path,
                    'detail': f'无法删除文件: {file_path}',
                    'success': False
                }
                
        except Exception as e:
            if self.verbose:
                print(f"清除文件时出错: {e}")
            return {
                'type': 'file',
                'action': 'error',
                'detail': f'清除文件时出错: {e}',
                'success': False
            }
    
    def delete_file(self, file_path):
        """删除文件"""
        try:
            # 尝试直接删除
            os.remove(file_path)
            return True
        except PermissionError:
            # 如果没有权限，尝试使用管理员权限
            if self.verbose:
                print(f"没有权限删除文件 {file_path}，尝试使用管理员权限...")
            return self.delete_file_as_admin(file_path)
        except Exception as e:
            if self.verbose:
                print(f"删除文件时出错: {e}")
            return False
    
    def delete_file_as_admin(self, file_path):
        """使用管理员权限删除文件"""
        try:
            # 在Windows上，可以使用subprocess调用del命令
            import subprocess
            result = subprocess.run(
                ['cmd', '/c', 'del', '/f', '/q', file_path],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            if self.verbose:
                print(f"使用管理员权限删除文件时出错: {e}")
            return False
    
    def clean_directory(self, directory_path):
        """清除目录"""
        results = []
        
        try:
            if not os.path.exists(directory_path):
                return [{
                    'type': 'directory',
                    'action': 'skipped',
                    'path': directory_path,
                    'detail': f'目录不存在: {directory_path}',
                    'success': False,
                    'skipped': True
                }]
            
            # 遍历目录中的所有文件和子目录
            for root, dirs, files in os.walk(directory_path, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    result = self.clean_file({'path': file_path})
                    results.append(result)
                
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    result = self.clean_directory_item(dir_path)
                    results.append(result)
            
            # 删除主目录
            result = self.clean_directory_item(directory_path)
            results.append(result)
            
            return results
            
        except Exception as e:
            if self.verbose:
                print(f"清除目录时出错: {e}")
            return [{
                'type': 'directory',
                'action': 'error',
                'path': directory_path,
                'detail': f'清除目录时出错: {e}',
                'success': False
            }]
    
    def clean_directory_item(self, dir_path):
        """清除目录项"""
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                return {
                    'type': 'directory',
                    'action': 'deleted',
                    'path': dir_path,
                    'detail': f'成功删除目录: {dir_path}',
                    'success': True
                }
            else:
                return {
                    'type': 'directory',
                    'action': 'skipped',
                    'path': dir_path,
                    'detail': f'目录不存在: {dir_path}',
                    'success': False,
                    'skipped': True
                }
        except Exception as e:
            if self.verbose:
                print(f"删除目录时出错: {e}")
            return {
                'type': 'directory',
                'action': 'failed',
                'path': dir_path,
                'detail': f'无法删除目录: {dir_path}',
                'success': False
            }
    
    def clean_all(self):
        """清除所有可疑文件"""
        results = []
        
        # 常见恶意文件路径
        malicious_paths = [
            r"C:\Program Files\Internet Explorer\log.dll",
            r"C:\Users\Public\Documents\malicious.dll",
            r"C:\Temp\payload.dll",
            r"C:\Windows\System32\svchost.exe"  # 注意：这个需要特别处理
        ]
        
        for path in malicious_paths:
            if os.path.exists(path):
                if os.path.isfile(path):
                    result = self.clean_file({'path': path})
                    results.append(result)
                elif os.path.isdir(path):
                    result = self.clean_directory(path)
                    results.extend(result)
        
        return results
    
    def is_malicious_file(self, file_path):
        """检查是否是恶意文件"""
        # 检查文件扩展名
        malicious_extensions = ['.dll', '.exe', '.msi', '.bat', '.cmd', '.vbs', '.js']
        if any(file_path.lower().endswith(ext) for ext in malicious_extensions):
            # 检查文件路径
            suspicious_paths = ['Temp', 'AppData', 'Downloads']
            if any(path in file_path for path in suspicious_paths):
                return True
        
        return False
    
    def backup_file(self, file_path):
        """备份文件"""
        try:
            backup_path = file_path + '.backup'
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            if self.verbose:
                print(f"备份文件时出错: {e}")
            return None
