#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IOC数据库模块
IOC Database Module
"""

from .file_hashes import MaliciousHashes
from .domains import MaliciousDomains
from .registry_keys import MaliciousRegistryKeys
from .files import MaliciousFiles
from .processes import MaliciousProcesses
from .ips import MaliciousIPs
from .ports import MaliciousPorts

class IOCDatabase:
    """IOC数据库"""
    
    def __init__(self):
        self.hashes = MaliciousHashes()
        self.domains = MaliciousDomains()
        self.registry_keys = MaliciousRegistryKeys()
        self.files = MaliciousFiles()
        self.processes = MaliciousProcesses()
        self.ips = MaliciousIPs()
        self.ports = MaliciousPorts()
    
    def get_all_iocs(self):
        """获取所有IOC"""
        return {
            'hashes': self.hashes.get_hashes(),
            'domains': self.domains.get_domains(),
            'registry_keys': self.registry_keys.get_all_keys(),
            'files': self.files.get_all_files(),
            'processes': self.processes.get_all_processes(),
            'ips': self.ips.get_ips(),
            'ports': self.ports.get_ports()
        }
    
    def update_iocs(self):
        """更新IOC数据库"""
        # 这里可以添加从远程服务器更新IOC的逻辑
        pass
