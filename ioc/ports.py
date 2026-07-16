#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恶意端口数据库
Malicious Ports Database - 银狐木马 IOC
"""

class MaliciousPorts:
    """恶意端口"""
    
    def __init__(self):
        # 银狐病毒已知的恶意端口
        self.ports = [
            # ========== 银狐专用端口 ==========
            8880,   # 银狐病毒回联端口（最常见）
            5050,   # ValleyRAT C2端口
            1080,   # 伪装Telegram C2端口
            9000,   # 远控C2端口
            27978,  # ValleyRAT C2端口
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
    
    def search_port(self, query):
        """搜索端口"""
        return [p for p in self.ports if str(query) in str(p)]
