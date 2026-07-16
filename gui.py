#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银狐病毒专杀工具 - 图形化界面
SilverFox Virus Killer - GUI
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import importlib
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class SilverFoxKillerGUI:
    """银狐病毒专杀工具图形化界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("银狐病毒专杀工具 v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置主题颜色
        self.bg_color = "#f0f0f0"
        self.accent_color = "#007bff"
        self.success_color = "#28a745"
        self.warning_color = "#ffc107"
        self.danger_color = "#dc3545"
        
        # 配置根窗口
        self.root.configure(bg=self.bg_color)
        
        # 创建界面
        self.create_widgets()
        
        # 初始化模块
        self.init_modules()
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(title_frame, text="银狐病毒专杀工具", font=("Arial", 24, "bold"))
        title_label.pack(side=tk.LEFT)
        
        version_label = ttk.Label(title_frame, text="v1.0", font=("Arial", 12))
        version_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 左侧控制面板
        control_frame = ttk.LabelFrame(main_frame, text="操作控制", padding="10")
        control_frame.grid(row=1, column=0, padx=(0, 10), sticky=(tk.N, tk.S))
        
        # 扫描按钮
        self.scan_btn = ttk.Button(control_frame, text="🔍 扫描系统", 
                                  command=self.start_scan, width=15)
        self.scan_btn.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # 清除按钮
        self.clean_btn = ttk.Button(control_frame, text="🧹 清除病毒", 
                                   command=self.start_clean, width=15, state=tk.DISABLED)
        self.clean_btn.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # 修复按钮
        self.repair_btn = ttk.Button(control_frame, text="🔧 修复系统", 
                                    command=self.start_repair, width=15, state=tk.DISABLED)
        self.repair_btn.grid(row=2, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # 完整处理按钮
        self.full_btn = ttk.Button(control_frame, text="⚡ 完整处理", 
                                  command=self.start_full, width=15)
        self.full_btn.grid(row=3, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # 分隔线
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).grid(row=4, column=0, 
                                                                pady=10, sticky=(tk.W, tk.E))
        
        # 进度条
        self.progress_label = ttk.Label(control_frame, text="就绪")
        self.progress_label.grid(row=5, column=0, pady=(5, 0))
        
        self.progress_bar = ttk.Progressbar(control_frame, mode='determinate', length=150)
        self.progress_bar.grid(row=6, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # 统计信息
        stats_frame = ttk.LabelFrame(control_frame, text="统计信息", padding="5")
        stats_frame.grid(row=7, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
        
        self.threats_label = ttk.Label(stats_frame, text="威胁: 0")
        self.threats_label.grid(row=0, column=0, sticky=tk.W)
        
        self.cleaned_label = ttk.Label(stats_frame, text="已清除: 0")
        self.cleaned_label.grid(row=1, column=0, sticky=tk.W)
        
        self.repaired_label = ttk.Label(stats_frame, text="已修复: 0")
        self.repaired_label.grid(row=2, column=0, sticky=tk.W)
        
        # 右侧结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="扫描结果", padding="10")
        result_frame.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # 结果树形视图
        columns = ("类型", "严重性", "路径", "详情")
        self.result_tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题
        self.result_tree.heading("类型", text="类型")
        self.result_tree.heading("严重性", text="严重性")
        self.result_tree.heading("路径", text="路径")
        self.result_tree.heading("详情", text="详情")
        
        # 设置列宽
        self.result_tree.column("类型", width=80)
        self.result_tree.column("严重性", width=80)
        self.result_tree.column("路径", width=200)
        self.result_tree.column("详情", width=250)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        self.result_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 底部日志区域
        log_frame = ttk.LabelFrame(main_frame, text="操作日志", padding="5")
        log_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # 配置日志文本框标签
        self.log_text.tag_configure("info", foreground="black")
        self.log_text.tag_configure("success", foreground="green")
        self.log_text.tag_configure("warning", foreground="orange")
        self.log_text.tag_configure("error", foreground="red")
    
    def init_modules(self):
        """初始化模块"""
        try:
            # 检查psutil
            try:
                import psutil
                self.log("psutil模块加载成功", "success")
            except ImportError:
                self.log("警告: psutil模块未安装，部分功能受限", "warning")
            
            from scanner import SilverFoxScanner
            from cleaner import SilverFoxCleaner
            修复_module = importlib.import_module('修复')
            SystemRepair = 修复_module.SystemRepair
            from reports import ReportGenerator
            
            self.scanner = SilverFoxScanner(verbose=True)
            self.cleaner = SilverFoxCleaner(verbose=True)
            self.repairer = SystemRepair(verbose=True)
            self.report_gen = ReportGenerator(verbose=True)
            
            self.log("模块初始化成功", "success")
            self.update_status("就绪")
            
        except Exception as e:
            self.log(f"模块初始化失败: {e}", "error")
            self.log(f"错误详情: {str(e)}", "error")
            messagebox.showerror("错误", f"模块初始化失败: {e}\n\n请确保已安装所有依赖：pip install psutil")
    
    def log(self, message, level="info"):
        """添加日志"""
        self.log_text.insert(tk.END, f"{message}\n", level)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, status):
        """更新状态"""
        self.progress_label.config(text=status)
        self.root.update_idletasks()
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar['value'] = value
        self.root.update_idletasks()
    
    def clear_results(self):
        """清空结果"""
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
    
    def add_result(self, result_type, severity, path, detail):
        """添加结果"""
        self.result_tree.insert("", tk.END, values=(result_type, severity, path, detail))
    
    def start_scan(self):
        """开始扫描"""
        self.clear_results()
        self.log("开始扫描系统...", "info")
        self.update_status("扫描中...")
        self.update_progress(0)
        
        # 禁用按钮
        self.scan_btn.config(state=tk.DISABLED)
        self.clean_btn.config(state=tk.DISABLED)
        self.repair_btn.config(state=tk.DISABLED)
        self.full_btn.config(state=tk.DISABLED)
        
        # 在新线程中执行扫描
        thread = threading.Thread(target=self.run_scan)
        thread.daemon = True
        thread.start()
    
    def run_scan(self):
        """执行扫描"""
        try:
            # 模拟进度
            for i in range(101):
                self.root.after(0, self.update_progress, i)
                time.sleep(0.02)
            
            # 执行扫描
            results = self.scanner.scan_all()
            
            # 更新结果
            self.root.after(0, self.scan_complete, results)
            
        except Exception as e:
            self.root.after(0, self.scan_error, str(e))
    
    def scan_complete(self, results):
        """扫描完成"""
        self.clear_results()
        
        for result in results:
            self.add_result(
                result.get('type', 'unknown'),
                result.get('severity', 'unknown'),
                result.get('path', 'N/A'),
                result.get('detail', 'N/A')
            )
        
        # 更新统计
        self.threats_label.config(text=f"威胁: {len(results)}")
        
        # 更新状态
        self.log(f"扫描完成，发现 {len(results)} 个威胁", "success" if len(results) == 0 else "warning")
        self.update_status("扫描完成")
        self.update_progress(100)
        
        # 启用按钮
        self.scan_btn.config(state=tk.NORMAL)
        if results:
            self.clean_btn.config(state=tk.NORMAL)
            self.repair_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
    
    def scan_error(self, error_msg):
        """扫描出错"""
        self.log(f"扫描出错: {error_msg}", "error")
        self.update_status("扫描失败")
        self.update_progress(0)
        
        # 启用按钮
        self.scan_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
        
        messagebox.showerror("扫描错误", f"扫描过程中出错: {error_msg}")
    
    def start_clean(self):
        """开始清除"""
        self.log("开始清除病毒...", "info")
        self.update_status("清除中...")
        self.update_progress(0)
        
        # 禁用按钮
        self.scan_btn.config(state=tk.DISABLED)
        self.clean_btn.config(state=tk.DISABLED)
        self.repair_btn.config(state=tk.DISABLED)
        self.full_btn.config(state=tk.DISABLED)
        
        # 在新线程中执行清除
        thread = threading.Thread(target=self.run_clean)
        thread.daemon = True
        thread.start()
    
    def run_clean(self):
        """执行清除"""
        try:
            # 模拟进度
            for i in range(101):
                self.root.after(0, self.update_progress, i)
                time.sleep(0.02)
            
            # 执行清除
            results = self.cleaner.clean_all()
            
            # 更新结果
            self.root.after(0, self.clean_complete, results)
            
        except Exception as e:
            self.root.after(0, self.clean_error, str(e))
    
    def clean_complete(self, results):
        """清除完成"""
        # 更新统计
        cleaned_count = sum(1 for r in results if r.get('success', False))
        self.cleaned_label.config(text=f"已清除: {cleaned_count}")
        
        # 更新状态
        self.log(f"清除完成，处理了 {len(results)} 个项目", "success")
        self.update_status("清除完成")
        self.update_progress(100)
        
        # 启用按钮
        self.scan_btn.config(state=tk.NORMAL)
        self.clean_btn.config(state=tk.NORMAL)
        self.repair_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
    
    def clean_error(self, error_msg):
        """清除出错"""
        self.log(f"清除出错: {error_msg}", "error")
        self.update_status("清除失败")
        self.update_progress(0)
        
        # 启用按钮
        self.scan_btn.config(state=tk.NORMAL)
        self.clean_btn.config(state=tk.NORMAL)
        self.repair_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
        
        messagebox.showerror("清除错误", f"清除过程中出错: {error_msg}")
    
    def start_repair(self):
        """开始修复"""
        self.log("开始修复系统...", "info")
        self.update_status("修复中...")
        self.update_progress(0)
        
        # 禁用按钮
        self.scan_btn.config(state=tk.DISABLED)
        self.clean_btn.config(state=tk.DISABLED)
        self.repair_btn.config(state=tk.DISABLED)
        self.full_btn.config(state=tk.DISABLED)
        
        # 在新线程中执行修复
        thread = threading.Thread(target=self.run_repair)
        thread.daemon = True
        thread.start()
    
    def run_repair(self):
        """执行修复"""
        try:
            # 模拟进度
            for i in range(101):
                self.root.after(0, self.update_progress, i)
                time.sleep(0.02)
            
            # 执行修复
            results = self.repairer.repair_all()
            
            # 更新结果
            self.root.after(0, self.repair_complete, results)
            
        except Exception as e:
            self.root.after(0, self.repair_error, str(e))
    
    def repair_complete(self, results):
        """修复完成"""
        # 更新统计
        repaired_count = sum(1 for r in results if r.get('success', False))
        self.repaired_label.config(text=f"已修复: {repaired_count}")
        
        # 更新状态
        self.log(f"修复完成，处理了 {len(results)} 个设置", "success")
        self.update_status("修复完成")
        self.update_progress(100)
        
        # 启用按钮
        self.scan_btn.config(state=tk.NORMAL)
        self.clean_btn.config(state=tk.NORMAL)
        self.repair_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
    
    def repair_error(self, error_msg):
        """修复出错"""
        self.log(f"修复出错: {error_msg}", "error")
        self.update_status("修复失败")
        self.update_progress(0)
        
        # 启用按钮
        self.scan_btn.config(state=tk.NORMAL)
        self.clean_btn.config(state=tk.NORMAL)
        self.repair_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
        
        messagebox.showerror("修复错误", f"修复过程中出错: {error_msg}")
    
    def start_full(self):
        """开始完整处理"""
        self.clear_results()
        self.log("开始完整处理（扫描+清除+修复）...", "info")
        self.update_status("完整处理中...")
        self.update_progress(0)
        
        # 禁用按钮
        self.scan_btn.config(state=tk.DISABLED)
        self.clean_btn.config(state=tk.DISABLED)
        self.repair_btn.config(state=tk.DISABLED)
        self.full_btn.config(state=tk.DISABLED)
        
        # 在新线程中执行完整处理
        thread = threading.Thread(target=self.run_full)
        thread.daemon = True
        thread.start()
    
    def run_full(self):
        """执行完整处理"""
        try:
            # 扫描阶段
            self.root.after(0, self.log, "阶段1/3: 扫描系统...", "info")
            for i in range(34):
                self.root.after(0, self.update_progress, i)
                time.sleep(0.02)
            
            scan_results = self.scanner.scan_all()
            self.root.after(0, self.log, f"扫描完成，发现 {len(scan_results)} 个威胁", "info")
            
            # 清除阶段
            self.root.after(0, self.log, "阶段2/3: 清除病毒...", "info")
            for i in range(34, 67):
                self.root.after(0, self.update_progress, i)
                time.sleep(0.02)
            
            clean_results = self.cleaner.clean_all(scan_results)
            self.root.after(0, self.log, f"清除完成，处理了 {len(clean_results)} 个项目", "info")
            
            # 修复阶段
            self.root.after(0, self.log, "阶段3/3: 修复系统...", "info")
            for i in range(67, 101):
                self.root.after(0, self.update_progress, i)
                time.sleep(0.02)
            
            repair_results = self.repairer.repair_all()
            self.root.after(0, self.log, f"修复完成，处理了 {len(repair_results)} 个设置", "info")
            
            # 更新结果
            self.root.after(0, self.full_complete, scan_results, clean_results, repair_results)
            
        except Exception as e:
            self.root.after(0, self.full_error, str(e))
    
    def full_complete(self, scan_results, clean_results, repair_results):
        """完整处理完成"""
        # 清空并更新结果
        self.clear_results()
        
        # 显示扫描结果
        for result in scan_results:
            self.add_result(
                result.get('type', 'unknown'),
                result.get('severity', 'unknown'),
                result.get('path', 'N/A'),
                result.get('detail', 'N/A')
            )
        
        # 更新统计
        self.threats_label.config(text=f"威胁: {len(scan_results)}")
        cleaned_count = sum(1 for r in clean_results if r.get('success', False))
        self.cleaned_label.config(text=f"已清除: {cleaned_count}")
        repaired_count = sum(1 for r in repair_results if r.get('success', False))
        self.repaired_label.config(text=f"已修复: {repaired_count}")
        
        # 更新状态
        self.log("完整处理完成！", "success")
        self.update_status("完整处理完成")
        self.update_progress(100)
        
        # 启用按钮
        self.scan_btn.config(state=tk.NORMAL)
        self.clean_btn.config(state=tk.NORMAL)
        self.repair_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
        
        messagebox.showinfo("完成", "完整处理已完成！请查看详细结果。")
    
    def full_error(self, error_msg):
        """完整处理出错"""
        self.log(f"完整处理出错: {error_msg}", "error")
        self.update_status("完整处理失败")
        self.update_progress(0)
        
        # 启用按钮
        self.scan_btn.config(state=tk.NORMAL)
        self.clean_btn.config(state=tk.NORMAL)
        self.repair_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
        
        messagebox.showerror("错误", f"完整处理过程中出错: {error_msg}")

def main():
    """主函数"""
    root = tk.Tk()
    app = SilverFoxKillerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
