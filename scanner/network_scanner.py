#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络扫描模块
Network Scanner Module
"""

import psutil
import socket
from ioc import MaliciousDomains, MaliciousIPs, MaliciousPorts

class NetworkScanner:
    """网络扫描器"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.malicious_domains = MaliciousDomains()
        self.malicious_ips = MaliciousIPs()
        self.malicious_ports = MaliciousPorts()
    
    def scan(self):
        """扫描网络连接"""
        results = []
        
        try:
            # 获取所有网络连接
            connections = psutil.net_connections()
            
            for conn in connections:
                try:
                    # 检查连接是否可疑
                    if self.is_suspicious_connection(conn):
                        results.append({
                            'type': 'network',
                            'severity': 'high',
                            'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A",
                            'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                            'status': conn.status,
                            'pid': conn.pid,
                            'detail': f'可疑网络连接',
                            'action': 'recommend_block'
                        })
                    
                    # 检查连接是否是恶意连接
                    elif self.is_malicious_connection(conn):
                        results.append({
                            'type': 'network',
                            'severity': 'critical',
                            'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A",
                            'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                            'status': conn.status,
                            'pid': conn.pid,
                            'detail': f'恶意网络连接',
                            'action': 'recommend_block'
                        })
                        
                except Exception as e:
                    if self.verbose:
                        print(f"检查连接时出错: {e}")
        
        except psutil.AccessDenied:
            if self.verbose:
                print("网络连接扫描需要管理员权限，跳过此步骤")
        except Exception as e:
            if self.verbose:
                print(f"获取网络连接时出错: {e}")
        
        return results
    
    def is_suspicious_connection(self, conn):
        """检查是否是可疑连接"""
        try:
            # 检查远程端口
            if conn.raddr:
                remote_port = conn.raddr.port
                if remote_port in self.malicious_ports.get_ports():
                    return True
                
                # 检查远程IP
                remote_ip = conn.raddr.ip
                if remote_ip in self.malicious_ips.get_ips():
                    return True
                
                # 检查远程域名（如果可以解析）
                try:
                    hostname = socket.gethostbyaddr(remote_ip)[0]
                    if self.is_malicious_domain(hostname):
                        return True
                except (socket.herror, socket.gaierror):
                    pass
            
            # 检查进程是否可疑
            if conn.pid:
                try:
                    proc = psutil.Process(conn.pid)
                    suspicious_processes = ['svchost.exe', 'explorer.exe', 'notepad.exe']
                    if proc.name() in suspicious_processes:
                        # 检查是否在异常路径
                        proc_path = proc.exe()
                        if proc_path and 'Temp' in proc_path:
                            return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            return False
            
        except Exception as e:
            if self.verbose:
                print(f"检查连接时出错: {e}")
            return False
    
    def is_malicious_connection(self, conn):
        """检查是否是恶意连接"""
        try:
            if conn.raddr:
                # 检查远程IP是否是恶意IP
                remote_ip = conn.raddr.ip
                if remote_ip in self.malicious_ips.get_ips():
                    return True
                
                # 检查远程端口是否是恶意端口
                remote_port = conn.raddr.port
                if remote_port in self.malicious_ports.get_ports():
                    return True
            
            return False
            
        except Exception as e:
            if self.verbose:
                print(f"检查连接时出错: {e}")
            return False
    
    def is_malicious_domain(self, domain):
        """检查是否是恶意域名"""
        malicious_domains = self.malicious_domains.get_domains()
        for malicious_domain in malicious_domains:
            if malicious_domain in domain:
                return True
        return False
    
    def get_connections_by_pid(self, pid):
        """根据PID获取网络连接"""
        connections = psutil.net_connections()
        return [conn for conn in connections if conn.pid == pid]
    
    def get_connections_by_status(self, status):
        """根据状态获取网络连接"""
        connections = psutil.net_connections()
        return [conn for conn in connections if conn.status == status]
    
    def get_established_connections(self):
        """获取已建立的连接"""
        return self.get_connections_by_status('ESTABLISHED')
    
    def get_listening_connections(self):
        """获取监听中的连接"""
        return self.get_connections_by_status('LISTEN')
