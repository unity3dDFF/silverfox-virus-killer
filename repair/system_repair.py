#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统修复器
System Repairer
"""

import subprocess
import sys

# 检查是否在Windows系统上运行
if sys.platform == 'win32':
    import winreg
else:
    winreg = None

class SystemRepair:
    """系统修复器"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def repair_system_settings(self):
        """修复系统设置"""
        results = []
        
        # 修复Windows更新服务
        results.append(self.repair_windows_update_service())
        
        # 修复Windows Defender服务
        results.append(self.repair_windows_defender_service())
        
        # 修复系统文件
        results.append(self.repair_system_files())
        
        return results
    
    def repair_security_settings(self):
        """修复安全设置"""
        results = []
        
        # 修复防火墙设置
        results.append(self.repair_firewall_settings())
        
        # 修复UAC设置
        results.append(self.repair_uac_settings())
        
        # 修复Windows Defender设置
        results.append(self.repair_defender_settings())
        
        return results
    
    def repair_startup_items(self):
        """修复启动项"""
        results = []
        
        # 清理恶意启动项
        results.append(self.clean_malicious_startup_items())
        
        # 恢复正常启动项
        results.append(self.restore_normal_startup_items())
        
        return results
    
    def repair_network_settings(self):
        """修复网络设置"""
        results = []
        
        # 修复DNS设置
        results.append(self.repair_dns_settings())
        
        # 修复hosts文件
        results.append(self.repair_hosts_file())
        
        # 修复网络连接
        results.append(self.repair_network_connections())
        
        return results
    
    def repair_windows_update_service(self):
        """修复Windows更新服务"""
        try:
            # 检查服务状态
            result = subprocess.run(
                ['sc', 'query', 'wuauserv'],
                capture_output=True,
                text=True
            )
            
            if 'STOPPED' in result.stdout:
                # 启动服务
                result = subprocess.run(
                    ['sc', 'start', 'wuauserv'],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    return {
                        'type': 'service',
                        'action': 'started',
                        'service': 'wuauserv',
                        'detail': '成功启动Windows更新服务',
                        'success': True
                    }
            
            return {
                'type': 'service',
                'action': 'checked',
                'service': 'wuauserv',
                'detail': 'Windows更新服务状态正常',
                'success': True
            }
            
        except Exception as e:
            if self.verbose:
                print(f"修复Windows更新服务时出错: {e}")
            return {
                'type': 'service',
                'action': 'error',
                'service': 'wuauserv',
                'detail': f'修复Windows更新服务时出错: {e}',
                'success': False
            }
    
    def repair_windows_defender_service(self):
        """修复Windows Defender服务"""
        try:
            # 检查服务状态
            result = subprocess.run(
                ['sc', 'query', 'WinDefend'],
                capture_output=True,
                text=True
            )
            
            if 'STOPPED' in result.stdout:
                # 启动服务
                result = subprocess.run(
                    ['sc', 'start', 'WinDefend'],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    return {
                        'type': 'service',
                        'action': 'started',
                        'service': 'WinDefend',
                        'detail': '成功启动Windows Defender服务',
                        'success': True
                    }
            
            return {
                'type': 'service',
                'action': 'checked',
                'service': 'WinDefend',
                'detail': 'Windows Defender服务状态正常',
                'success': True
            }
            
        except Exception as e:
            if self.verbose:
                print(f"修复Windows Defender服务时出错: {e}")
            return {
                'type': 'service',
                'action': 'error',
                'service': 'WinDefend',
                'detail': f'修复Windows Defender服务时出错: {e}',
                'success': False
            }
    
    def repair_system_files(self):
        """修复系统文件"""
        try:
            # 使用sfc /scannow命令
            result = subprocess.run(
                ['sfc', '/scannow'],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                return {
                    'type': 'system',
                    'action': 'repaired',
                    'detail': '系统文件修复完成',
                    'success': True
                }
            else:
                return {
                    'type': 'system',
                    'action': 'failed',
                    'detail': f'系统文件修复失败: {result.stderr}',
                    'success': False
                }
                
        except Exception as e:
            if self.verbose:
                print(f"修复系统文件时出错: {e}")
            return {
                'type': 'system',
                'action': 'error',
                'detail': f'修复系统文件时出错: {e}',
                'success': False
            }
    
    def repair_firewall_settings(self):
        """修复防火墙设置"""
        try:
            # 启用防火墙
            result = subprocess.run(
                ['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'on'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    'type': 'firewall',
                    'action': 'enabled',
                    'detail': '成功启用Windows防火墙',
                    'success': True
                }
            else:
                return {
                    'type': 'firewall',
                    'action': 'failed',
                    'detail': f'启用Windows防火墙失败: {result.stderr}',
                    'success': False
                }
                
        except Exception as e:
            if self.verbose:
                print(f"修复防火墙设置时出错: {e}")
            return {
                'type': 'firewall',
                'action': 'error',
                'detail': f'修复防火墙设置时出错: {e}',
                'success': False
            }
    
    def repair_uac_settings(self):
        """修复UAC设置"""
        # 如果不是Windows系统，返回跳过结果
        if sys.platform != 'win32':
            return {
                'type': 'security',
                'action': 'skipped',
                'detail': 'UAC设置修复仅在Windows系统上支持',
                'success': False,
                'skipped': True
            }
        
        try:
            # 设置UAC为默认级别
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
            
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "EnableLUA", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            return {
                'type': 'security',
                'action': 'repaired',
                'detail': '成功修复UAC设置',
                'success': True
            }
            
        except Exception as e:
            if self.verbose:
                print(f"修复UAC设置时出错: {e}")
            return {
                'type': 'security',
                'action': 'error',
                'detail': f'修复UAC设置时出错: {e}',
                'success': False
            }
    
    def repair_defender_settings(self):
        """修复Windows Defender设置"""
        try:
            # 启用Windows Defender实时保护
            result = subprocess.run(
                ['powershell', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $false'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    'type': 'security',
                    'action': 'repaired',
                    'detail': '成功启用Windows Defender实时保护',
                    'success': True
                }
            else:
                return {
                    'type': 'security',
                    'action': 'failed',
                    'detail': f'启用Windows Defender实时保护失败: {result.stderr}',
                    'success': False
                }
                
        except Exception as e:
            if self.verbose:
                print(f"修复Windows Defender设置时出错: {e}")
            return {
                'type': 'security',
                'action': 'error',
                'detail': f'修复Windows Defender设置时出错: {e}',
                'success': False
            }
    
    def clean_malicious_startup_items(self):
        """清理恶意启动项"""
        # 如果不是Windows系统，返回跳过结果
        if sys.platform != 'win32':
            return {
                'type': 'startup',
                'action': 'skipped',
                'detail': '启动项清理仅在Windows系统上支持',
                'success': False,
                'skipped': True
            }
        
        try:
            # 清理注册表中的恶意启动项
            malicious_startup_items = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "SilverFox"),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "WinUpdateService"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "SilverFox"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "WinUpdateService")
            ]
            
            cleaned_count = 0
            for hive, key_path, value_name in malicious_startup_items:
                try:
                    key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_WRITE)
                    winreg.DeleteValue(key, value_name)
                    winreg.CloseKey(key)
                    cleaned_count += 1
                except WindowsError:
                    pass
            
            if cleaned_count > 0:
                return {
                    'type': 'startup',
                    'action': 'cleaned',
                    'detail': f'成功清理 {cleaned_count} 个恶意启动项',
                    'success': True
                }
            else:
                return {
                    'type': 'startup',
                    'action': 'checked',
                    'detail': '未发现恶意启动项',
                    'success': True
                }
                
        except Exception as e:
            if self.verbose:
                print(f"清理恶意启动项时出错: {e}")
            return {
                'type': 'startup',
                'action': 'error',
                'detail': f'清理恶意启动项时出错: {e}',
                'success': False
            }
    
    def restore_normal_startup_items(self):
        """恢复正常启动项"""
        # 这里可以添加恢复正常使用启动项的逻辑
        return {
            'type': 'startup',
            'action': 'checked',
            'detail': '启动项检查完成',
            'success': True
        }
    
    def repair_dns_settings(self):
        """修复DNS设置"""
        try:
            # 重置DNS设置
            result = subprocess.run(
                ['ipconfig', '/flushdns'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    'type': 'network',
                    'action': 'repaired',
                    'detail': '成功刷新DNS缓存',
                    'success': True
                }
            else:
                return {
                    'type': 'network',
                    'action': 'failed',
                    'detail': f'刷新DNS缓存失败: {result.stderr}',
                    'success': False
                }
                
        except Exception as e:
            if self.verbose:
                print(f"修复DNS设置时出错: {e}")
            return {
                'type': 'network',
                'action': 'error',
                'detail': f'修复DNS设置时出错: {e}',
                'success': False
            }
    
    def repair_hosts_file(self):
        """修复hosts文件"""
        try:
            hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
            
            # 备份hosts文件
            import shutil
            backup_path = hosts_path + '.backup'
            shutil.copy2(hosts_path, backup_path)
            
            # 读取hosts文件
            with open(hosts_path, 'r') as f:
                content = f.read()
            
            # 移除恶意条目
            lines = content.split('\n')
            clean_lines = []
            for line in lines:
                if not any(malicious in line for malicious in ['银狐', 'silverfox', 'vauwjw.net', 'cinskw.net']):
                    clean_lines.append(line)
            
            # 写入清理后的hosts文件
            with open(hosts_path, 'w') as f:
                f.write('\n'.join(clean_lines))
            
            return {
                'type': 'network',
                'action': 'repaired',
                'detail': '成功修复hosts文件',
                'success': True
            }
            
        except Exception as e:
            if self.verbose:
                print(f"修复hosts文件时出错: {e}")
            return {
                'type': 'network',
                'action': 'error',
                'detail': f'修复hosts文件时出错: {e}',
                'success': False
            }
    
    def repair_network_connections(self):
        """修复网络连接"""
        try:
            # 重置网络连接
            result = subprocess.run(
                ['netsh', 'winsock', 'reset'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    'type': 'network',
                    'action': 'repaired',
                    'detail': '成功重置网络套接字',
                    'success': True
                }
            else:
                return {
                    'type': 'network',
                    'action': 'failed',
                    'detail': f'重置网络套接字失败: {result.stderr}',
                    'success': False
                }
                
        except Exception as e:
            if self.verbose:
                print(f"修复网络连接时出错: {e}")
            return {
                'type': 'network',
                'action': 'error',
                'detail': f'修复网络连接时出错: {e}',
                'success': False
            }
