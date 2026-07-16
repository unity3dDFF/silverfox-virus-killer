#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史记录模块
Scan/Clean/Repair History Manager
"""

import os
import json
import time
from datetime import datetime
from quarantine import default_data_dir


class ScanHistory:
    """扫描/清理/修复历史记录管理"""
    
    def __init__(self, history_dir=None):
        """初始化历史记录管理器"""
        if history_dir is None:
            history_dir = str(default_data_dir() / "History")
        
        self.history_dir = history_dir
        self.history_file = os.path.join(history_dir, "scan_history.json")
        self.max_records = 100  # 最大记录数
        
        # 确保目录存在
        os.makedirs(history_dir, exist_ok=True)
        
        # 加载历史记录
        self.records = self._load_history()
    
    def _load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载历史记录失败: {e}")
        return []
    
    def _save_history(self):
        """保存历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {e}")
    
    def add_record(self, action_type, results, summary=""):
        """
        添加新记录
        
        Args:
            action_type: 操作类型 (scan/clean/repair/full)
            results: 扫描/清理结果列表
            summary: 摘要信息
        """
        record = {
            "id": int(time.time() * 1000),
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "summary": summary,
            "result_count": len(results) if results else 0,
            "results": results[:50],  # 只保存前50条详细结果
            "truncated": len(results) > 50 if results else False,
        }
        
        # 添加到记录列表开头
        self.records.insert(0, record)
        
        # 限制记录数量
        if len(self.records) > self.max_records:
            self.records = self.records[:self.max_records]
        
        # 保存
        self._save_history()
        
        return record["id"]
    
    def get_records(self, limit=20, action_type=None):
        """
        获取历史记录
        
        Args:
            limit: 返回记录数量限制
            action_type: 筛选操作类型
            
        Returns:
            历史记录列表
        """
        records = self.records
        
        if action_type:
            records = [r for r in records if r.get("action_type") == action_type]
        
        return records[:limit]
    
    def get_record_by_id(self, record_id):
        """根据ID获取单条记录"""
        for record in self.records:
            if record.get("id") == record_id:
                return record
        return None
    
    def get_record_count(self):
        """获取记录总数"""
        return len(self.records)
    
    def clear_history(self):
        """清空所有历史记录"""
        self.records = []
        self._save_history()
    
    def delete_record(self, record_id):
        """删除单条记录"""
        self.records = [r for r in self.records if r.get("id") != record_id]
        self._save_history()
    
    def get_statistics(self):
        """获取统计信息"""
        stats = {
            "total_records": len(self.records),
            "scan_count": 0,
            "clean_count": 0,
            "repair_count": 0,
            "full_count": 0,
            "total_threats_found": 0,
            "total_threats_cleaned": 0,
        }
        
        for record in self.records:
            action = record.get("action_type", "")
            if action == "scan":
                stats["scan_count"] += 1
            elif action == "clean":
                stats["clean_count"] += 1
            elif action == "repair":
                stats["repair_count"] += 1
            elif action == "full":
                stats["full_count"] += 1
            
            stats["total_threats_found"] += record.get("result_count", 0)
        
        return stats
    
    def format_timestamp(self, iso_string):
        """格式化时间戳为可读格式"""
        try:
            dt = datetime.fromisoformat(iso_string)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return iso_string
    
    def get_action_type_name(self, action_type):
        """获取操作类型的中文名称"""
        type_names = {
            "scan": "扫描",
            "clean": "清理",
            "repair": "修复",
            "full": "全面处理",
        }
        return type_names.get(action_type, action_type)
