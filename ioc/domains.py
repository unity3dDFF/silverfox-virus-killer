#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恶意域名数据库
Malicious Domains Database - 银狐木马 IOC
"""

class MaliciousDomains:
    """恶意域名"""
    
    def __init__(self):
        # 银狐病毒已知的恶意域名
        self.domains = [
            # ========== 2026年7月 - ValleyRAT C2 ==========
            "3w.jxuw3.com",
            "df.sjickdeh.org",
            
            # ========== 2026年7月 - 邮件投递 ==========
            "frehf.oss-cn-hongkong.aliyuncs.com",
            
            # ========== 2026年5-6月 - Python stealer C2 ==========
            "xqwmwru.top",
            "9010.360sdgg.com",
            
            # ========== 2026年5月 - 钓鱼站点 ==========
            "cn-hk-oss-vip.com",
            
            # ========== 2026年3月 - 钓鱼域名 ==========
            "xxs.sckca.top",
            "hldfke.com",
            "xxs.z3m4.top",
            "xxxjjj250711.com",
            
            # ========== 2026年1月 - 伪装Telegram C2 ==========
            "v2.egrfbumsu.cn",
            "vnc.kcii2.com",
            
            # ========== 2025-2026年 - ABCDoor C2 ==========
            # (abc.* 三级域名模式)
            
            # ========== 阿里云OSS域名 ==========
            "omss.oss-cn-hangzhou.aliyuncs.com",
            "upitem.oss-cn-hangzhou.aliyuncs.com",
            "1o2.oss-cn-beijing.aliyuncs.com",
            "25o.oss-cn-beijing.aliyuncs.com",
            "98o.oss-cn-beijing.aliyuncs.com",
            "nm25.oss-cn-hangzhou.aliyuncs.com",
            
            # ========== 腾讯云COS域名 ==========
            "6-1321729461.cos.ap-guangzhou.myqcloud.com",
            "00-1321729461.cos.ap-guangzhou.myqcloud.com",
            
            # ========== 其他恶意域名 ==========
            "vauwjw.net",
            "cinskw.net",
            "hucgiu.net",
            "gqsqoq.net",
            "m-2.jplong.org",
            "vdcfdxstyy.cn",
            "emailqy.com",
            "shuiwutg.com",
            "shuiwutg1.cn",
            "shuiwutg2.cn",
            "shuiwutg3.cn",
            "shuiwutg4.cn",
            "shuiwujc0.cn",
            "shuiwujc1.cn",
            "cc.kmsccadn.com",
        ]
        self.domains = [domain.lower().rstrip('.') for domain in self.domains]
    
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
        domain = domain.lower().rstrip('.')
        return any(domain == item or domain.endswith('.' + item) for item in self.domains)
    
    def get_domain_count(self):
        """获取恶意域名数量"""
        return len(self.domains)
    
    def get_domains_by_provider(self, provider):
        """根据提供商获取域名"""
        return [domain for domain in self.domains if provider in domain]
    
    def search_domain(self, query):
        """搜索域名（支持部分匹配）"""
        query_lower = query.lower()
        return [d for d in self.domains if query_lower in d.lower()]
