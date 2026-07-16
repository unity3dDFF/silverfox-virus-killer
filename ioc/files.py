#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恶意文件数据库
Malicious Files Database - 银狐木马 IOC
"""

class MaliciousFiles:
    """恶意文件"""
    
    def __init__(self):
        # 银狐病毒已知的恶意文件
        self.malicious_files = {
            # 恶意文件名
            "filenames": [
                # ========== 2026年7月 - 伪装Steam/Telegram ==========
                "Steam.exe",
                "Telegram简体中文语言包.exe",
                
                # ========== 2026年5-6月 - 钓鱼文件 ==========
                "Yifanyi_setup_8.37_1747795776.exe",
                
                # ========== 2026年3月 - 伪装软件 ==========
                "CMake安装包.exe",
                "chrome-安装包.exe",
                "360SysVulTerminator.exe",
                
                # ========== 2026年1月 - 伪装Chrome ==========
                "ChromeSetup.exe",
                "ChromeSetup-9037.msi",
                "OTGContainer.exe",
                "FFLOADER.exe",
                "TelegramInst_setup_x64_250106.exe",
                
                # ========== 2025-2026年 - 网易CC借壳 ==========
                "yjwj_updater.exe",
                "yjwj_patcher.exe",
                
                # ========== 银狐通用恶意文件 ==========
                "开票-目录.exe",
                "违规-告示.exe",
                "违规-记录（1）.rar",
                "金稅四期（电脑版）-uninstall.msi",
                "金稅五期（电脑版）-uninstall.zip",
                "违纪名单.exe",
                "违纪通报信息.exe",
                "裁员名单.exe",
                "补偿方案.exe",
                "内部调查结果.exe",
                "2025年度各单位内制人员违纪名单.exe.zip",
                
                # ========== 投递文件 ==========
                "4TUnSLtk.exe",
                "ND9sxX58.exe",
                "6d6ba2bc9ad414837826f7278bc3e0116f1aeda02d0c2284ed65819f5d9180a8.exe",
                "查看10.exe",
                
                # ========== 白加黑组件 ==========
                "QMUpload.exe",
                "QMStuck.dll",
                "DyCrashRpt.dll",
                "kin.exe",
                "tracerpt.exe.dll",
                "libcurl.dll",
                "NtHandleCallback.exe",
                "main.exe",
                "bypass.exe",
                "KGseKKdKce.exe",
                "NVIDIA.exe",
                "tree.exe",
                "kail.exe",
                "edr.key",
                "me.key",
                
                # ========== 驱动文件 ==========
                "Cndom6.sys",
                "XiaoH.sys",
                "BdApiUtil64.sys",
                "rwdriver.sys",
                "NSecKrnl.sys",
                "kernelquick.sys",
                "189atohci.sys",
                "tProtect.dll",
                
                # ========== 配置/数据文件 ==========
                "bb.jpg",
                "rbg",
                "Server.log",
                "server8888",
                "Windows.log",
                "unins000.dat",
                "0710.exe",
                "locale.dat",
                "locale2.dat",
                "locale7.dat",
                "mainZTtRjTfyhNIDCAF.xml",
                "man50.dat",
                "men.exe",
                "setup.exe",
                "funzip.exe",
                "kail.exe",
                "winnt.exe",
                "runtime.exe",
                "destopbak.ini",
                "xpclnx.dll",
                "updat4.vac",
                "SSRClient.exe",
                "R2-Signed.exe",
                "npwzwmc64.dll",
                "gzwxQMIq.dat",
                "XPSPLOG.dll",
                "guardian_3b9bc840.ps1",
                "Microsoftdata.exe",
                "Xps.dtd",
            ],
            
            # 恶意文件路径
            "paths": [
                r"C:\Drivers",
                r"C:\Windows\System32",
                r"C:\Users\Public\Documents\WindowsData",
                r"C:\Users\Public\Downloads\bb.jpg",
                r"C:\Users\Public\Documents",
                r"C:\ProgramData",
                r"C:\Program Files\Internet Explorer\log.dll",
                r"C:\Temp",
                r"C:\Windows\Temp",
                r"C:\Users\*\AppData\Local\Temp",
                r"C:\WhatsAppBackup",
                r"C:\Users\Public\Download\bb.jpg",
            ],
            
            # 恶意文件扩展名
            "extensions": [
                ".dll",
                ".exe",
                ".msi",
                ".bat",
                ".cmd",
                ".vbs",
                ".js",
                ".ps1",
                ".sys",
                ".dat",
                ".key",
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
    
    def search_filename(self, query):
        """搜索文件名（支持部分匹配）"""
        query_lower = query.lower()
        return [f for f in self.malicious_files["filenames"] if query_lower in f.lower()]
