#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恶意文件数据库
Malicious Files Database
"""

class MaliciousFiles:
    """恶意文件"""
    
    def __init__(self):
        # 银狐病毒已知的恶意文件
        self.malicious_files = {
            # 常见恶意文件名
            "filenames": [
                "开票-目录.exe",
                "违规-告示.exe",
                "违规-记录（1）.rar",
                "金稅四期（电脑版）-uninstall.msi",
                "金稅五期（电脑版）-uninstall.zip",
                "违纪名单.exe",
                "裁员名单.exe",
                "补偿方案.exe",
                "内部调查结果.exe",
                "违纪通报信息.exe"
            ],
            
            # 常见恶意文件路径
            "paths": [
                r"C:\Program Files\Internet Explorer\log.dll",
                r"C:\Users\Public\Documents\malicious.dll",
                r"C:\Temp\payload.dll",
                r"C:\Windows\System32\svchost.exe",  # 注意：这个需要特别处理
                r"C:\Users\*\AppData\Local\Temp\*.dll",
                r"C:\Users\*\Downloads\*.exe"
            ],
            
            # 常见恶意文件扩展名
            "extensions": [
                ".dll",
                ".exe",
                ".msi",
                ".bat",
                ".cmd",
                ".vbs",
                ".js"
            ]
        }
    
    def get_all_files(self):
        """获取所有恶意文件信息"""
        return self.malicious_files
    
    def get_filenames(self):
        """获取恶意文件名"""
        return self.malicious_files.get("filenames", [])
    
    def get_paths(self):
        """获取恶意文件路径"""
        return self.malicious_files.get("paths", [])
    
    def get_extensions(self):
        """获取恶意文件扩展名"""
        return self.malicious_files.get("extensions", [])
    
    def add_filename(self, filename):
        """添加新的恶意文件名"""
        if filename not in self.malicious_files["filenames"]:
            self.malicious_files["filenames"].append(filename)
    
    def add_path(self, path):
        """添加新的恶意文件路径"""
        if path not in self.malicious_files["paths"]:
            self.malicious_files["paths"].append(path)
    
    def add_extension(self, extension):
        """添加新的恶意文件扩展名"""
        if extension not in self.malicious_files["extensions"]:
            self.malicious_files["extensions"].append(extension)
    
    def is_malicious_filename(self, filename):
        """检查文件名是否是恶意的"""
        return filename in self.malicious_files["filenames"]
    
    def is_malicious_path(self, file_path):
        """检查文件路径是否是恶意的"""
        for path in self.malicious_files["paths"]:
            if '*' in path:
                # 处理通配符路径
                import glob
                for expanded_path in glob.glob(path):
                    if file_path.startswith(expanded_path):
                        return True
            else:
                if file_path.startswith(path):
                    return True
        return False
    
    def is_malicious_extension(self, filename):
        """检查文件扩展名是否是恶意的"""
        for extension in self.malicious_files["extensions"]:
            if filename.lower().endswith(extension):
                return True
        return False
    
    def get_file_count(self):
        """获取恶意文件数量"""
        return len(self.malicious_files["filenames"])
