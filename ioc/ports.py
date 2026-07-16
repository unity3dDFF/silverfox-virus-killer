#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恶意端口数据库
Malicious Ports Database
"""

class MaliciousPorts:
    """恶意端口"""
    
    def __init__(self):
        # 银狐病毒已知的恶意端口
        self.ports = [
            # 常见恶意端口
            8880,  # 银狐病毒回联端口
            4444,  # 常见反弹shell端口
            5555,  # 常见远程控制端口
            6666,  # 常见恶意软件端口
            7777,  # 常见恶意软件端口
            8888,  # 常见恶意软件端口
            9999,  # 常见恶意软件端口
            
            # 更多端口...
        ]
    
    def get_ports(self):
        """获取所有恶意端口"""
        return self.ports
    
    def add_port(self, port):
        """添加新的恶意端口"""
        if port not in self.ports:
            self.ports.append(port)
    
    def remove_port(self, port):
        """移除恶意端口"""
        if port in self.ports:
            self.ports.remove(port)
    
    def is_malicious(self, port):
        """检查端口是否是恶意的"""
        return port in self.ports
    
    def get_port_count(self):
        """获取恶意端口数量"""
        return len(self.ports)
    
    def get_ports_by_service(self, service):
        """根据服务获取端口"""
        # 这里可以添加根据服务筛选端口的逻辑
        return self.ports
