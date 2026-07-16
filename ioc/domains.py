#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恶意域名数据库
Malicious Domains Database
"""

class MaliciousDomains:
    """恶意域名"""
    
    def __init__(self):
        # 银狐病毒已知的恶意域名
        self.domains = [
            # 阿里云OSS域名
            "omss.oss-cn-hangzhou.aliyuncs.com",
            "upitem.oss-cn-hangzhou.aliyuncs.com",
            "1o2.oss-cn-beijing.aliyuncs.com",
            "25o.oss-cn-beijing.aliyuncs.com",
            "98o.oss-cn-beijing.aliyuncs.com",
            
            # 其他恶意域名
            "vauwjw.net",
            "cinskw.net",
            "hucgiu.net",
            
            # 示例域名（需要实际替换）
            "example-malicious-domain.com",
            
            # 更多域名...
        ]
    
    def get_domains(self):
        """获取所有恶意域名"""
        return self.domains
    
    def add_domain(self, domain):
        """添加新的恶意域名"""
        if domain not in self.domains:
            self.domains.append(domain)
    
    def remove_domain(self, domain):
        """移除恶意域名"""
        if domain in self.domains:
            self.domains.remove(domain)
    
    def is_malicious(self, domain):
        """检查域名是否是恶意的"""
        for malicious_domain in self.domains:
            if malicious_domain in domain:
                return True
        return False
    
    def get_domain_count(self):
        """获取恶意域名数量"""
        return len(self.domains)
    
    def get_domains_by_provider(self, provider):
        """根据提供商获取域名"""
        return [domain for domain in self.domains if provider in domain]
