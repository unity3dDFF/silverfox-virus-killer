#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银狐病毒专杀工具 - 图形化界面
SilverFox Virus Killer - GUI
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, simpledialog
import threading
import importlib
import time
import subprocess
import platform
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class SilverFoxKillerGUI:
    """银狐病毒专杀工具图形化界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("银狐病毒专杀工具 v2.0")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # 设置主题颜色
        self.bg_color = "#f0f0f0"
        self.accent_color = "#007bff"
        self.success_color = "#28a745"
        self.warning_color = "#ffc107"
        self.danger_color = "#dc3545"
        
        # 配置根窗口
        self.root.configure(bg=self.bg_color)
        
        # 白名单文件
        self.whitelist_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "whitelist.json")
        self.whitelist = self._load_whitelist()
        
        # 初始化模块
        self.scanner = None
        self.cleaner = None
        self.repairer = None
        self.report_gen = None
        self.history = None
        
        # 创建界面
        self.create_widgets()
        
        # 初始化模块
        self.init_modules()
    
    def _load_whitelist(self):
        """加载白名单"""
        try:
            if os.path.exists(self.whitelist_file):
                with open(self.whitelist_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def _save_whitelist(self):
        """保存白名单"""
        try:
            with open(self.whitelist_file, 'w', encoding='utf-8') as f:
                json.dump(self.whitelist, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log(f"保存白名单失败: {e}", "error")
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 标题
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(title_frame, text="银狐病毒专杀工具", font=("Arial", 24, "bold"))
        title_label.pack(side=tk.LEFT)
        
        version_label = ttk.Label(title_frame, text="v2.0", font=("Arial", 12))
        version_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 使用 Notebook (标签页) 来组织内容
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # ===== 标签页1: 扫描清理 =====
        self.scan_tab = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(self.scan_tab, text="🔍 扫描清理")
        self._create_scan_tab()
        
        # ===== 标签页2: 历史记录 =====
        self.history_tab = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(self.history_tab, text="📋 历史记录")
        self._create_history_tab()
        
        # ===== 标签页3: 白名单管理 =====
        self.whitelist_tab = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(self.whitelist_tab, text="✅ 白名单管理")
        self._create_whitelist_tab()
    
    def _create_scan_tab(self):
        """创建扫描清理标签页"""
        self.scan_tab.columnconfigure(1, weight=1)
        self.scan_tab.rowconfigure(0, weight=1)
        
        # 左侧控制面板
        control_frame = ttk.LabelFrame(self.scan_tab, text="操作控制", padding="10")
        control_frame.grid(row=0, column=0, padx=(0, 10), sticky=(tk.N, tk.S))
        
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
        result_frame = ttk.LabelFrame(self.scan_tab, text="扫描结果 (右键可查看更多操作)", padding="5")
        result_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
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
        self.result_tree.column("路径", width=300)
        self.result_tree.column("详情", width=250)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        self.result_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 绑定右键菜单
        self.result_tree.bind("<Button-3>", self._show_context_menu)
        self.result_tree.bind("<Double-1>", self._on_double_click)
        
        # 创建右键菜单
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="📂 打开文件所在位置", command=self._open_file_location)
        self.context_menu.add_command(label="📋 复制文件路径", command=self._copy_file_path)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 复制完整路径", command=self._copy_full_path)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="➕ 添加到白名单", command=self._add_to_whitelist)
        self.context_menu.add_command(label="🗑️ 删除文件", command=self._delete_file)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🔍 在资源管理器中选择", command=self._reveal_in_explorer)
        self.context_menu.add_command(label="📝 查看详细信息", command=self._view_details)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📤 导出选中项", command=self._export_selected)
        self.context_menu.add_command(label="📤 导出全部", command=self._export_all)
        
        # 底部日志区域
        log_frame = ttk.LabelFrame(self.scan_tab, text="操作日志", padding="5")
        log_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # 配置日志文本框标签
        self.log_text.tag_configure("info", foreground="black")
        self.log_text.tag_configure("success", foreground="green")
        self.log_text.tag_configure("warning", foreground="orange")
        self.log_text.tag_configure("error", foreground="red")
    
    def _create_history_tab(self):
        """创建历史记录标签页"""
        self.history_tab.columnconfigure(0, weight=1)
        self.history_tab.rowconfigure(1, weight=1)
        
        # 顶部工具栏
        toolbar_frame = ttk.Frame(self.history_tab)
        toolbar_frame.grid(row=0, column=0, pady=(0, 5), sticky=(tk.W, tk.E))
        
        ttk.Button(toolbar_frame, text="🔄 刷新", command=self._refresh_history, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="🗑️ 清空历史", command=self._clear_history, width=10).pack(side=tk.LEFT, padx=2)
        
        # 筛选下拉框
        ttk.Label(toolbar_frame, text="  筛选:").pack(side=tk.LEFT, padx=(10, 2))
        self.history_filter = ttk.Combobox(toolbar_frame, values=["全部", "扫描", "清理", "修复", "完整处理"], 
                                            state="readonly", width=10)
        self.history_filter.set("全部")
        self.history_filter.pack(side=tk.LEFT, padx=2)
        self.history_filter.bind("<<ComboboxSelected>>", lambda e: self._refresh_history())
        
        # 统计标签
        self.history_stats_label = ttk.Label(toolbar_frame, text="共 0 条记录")
        self.history_stats_label.pack(side=tk.RIGHT, padx=5)
        
        # 历史记录列表
        list_frame = ttk.Frame(self.history_tab)
        list_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        columns = ("时间", "操作类型", "发现威胁数", "摘要")
        self.history_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        self.history_tree.heading("时间", text="时间")
        self.history_tree.heading("操作类型", text="操作类型")
        self.history_tree.heading("发现威胁数", text="发现威胁数")
        self.history_tree.heading("摘要", text="摘要")
        
        self.history_tree.column("时间", width=160)
        self.history_tree.column("操作类型", width=100)
        self.history_tree.column("发现威胁数", width=100)
        self.history_tree.column("摘要", width=400)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 绑定双击查看详情
        self.history_tree.bind("<Double-1>", self._view_history_detail)
        
        # 创建历史记录右键菜单
        self.history_context_menu = tk.Menu(self.root, tearoff=0)
        self.history_context_menu.add_command(label="📝 查看详情", command=self._view_history_detail_menu)
        self.history_context_menu.add_command(label="🔄 重新执行此扫描", command=self._replay_history)
        self.history_context_menu.add_separator()
        self.history_context_menu.add_command(label="🗑️ 删除此记录", command=self._delete_history_record)
        
        self.history_tree.bind("<Button-3>", self._show_history_context_menu)
        
        # 底部详情区域
        detail_frame = ttk.LabelFrame(self.history_tab, text="记录详情", padding="5")
        detail_frame.grid(row=2, column=0, pady=(5, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
        detail_frame.columnconfigure(0, weight=1)
        detail_frame.rowconfigure(0, weight=1)
        
        self.history_detail_text = scrolledtext.ScrolledText(detail_frame, height=6, wrap=tk.WORD)
        self.history_detail_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    
    def _create_whitelist_tab(self):
        """创建白名单管理标签页"""
        self.whitelist_tab.columnconfigure(0, weight=1)
        self.whitelist_tab.rowconfigure(1, weight=1)
        
        # 顶部工具栏
        toolbar_frame = ttk.Frame(self.whitelist_tab)
        toolbar_frame.grid(row=0, column=0, pady=(0, 5), sticky=(tk.W, tk.E))
        
        ttk.Button(toolbar_frame, text="➕ 添加路径", command=self._add_whitelist_item, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="➖ 移除选中", command=self._remove_whitelist_item, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="🔄 刷新", command=self._refresh_whitelist, width=10).pack(side=tk.LEFT, padx=2)
        
        # 白名单列表
        list_frame = ttk.Frame(self.whitelist_tab)
        list_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        columns = ("序号", "路径", "添加时间", "备注")
        self.whitelist_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        self.whitelist_tree.heading("序号", text="序号")
        self.whitelist_tree.heading("路径", text="路径")
        self.whitelist_tree.heading("添加时间", text="添加时间")
        self.whitelist_tree.heading("备注", text="备注")
        
        self.whitelist_tree.column("序号", width=60)
        self.whitelist_tree.column("路径", width=500)
        self.whitelist_tree.column("添加时间", width=150)
        self.whitelist_tree.column("备注", width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.whitelist_tree.yview)
        self.whitelist_tree.configure(yscrollcommand=scrollbar.set)
        
        self.whitelist_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 底部说明
        info_frame = ttk.LabelFrame(self.whitelist_tab, text="说明", padding="5")
        info_frame.grid(row=2, column=0, pady=(5, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(info_frame, text="• 白名单中的文件/路径在扫描时将被忽略\n"
                                    "• 可以是完整文件路径或目录路径\n"
                                    "• 支持通配符 (如 C:\\Program Files\\*\\safe.exe)",
                  foreground="gray").pack(anchor=tk.W)
        
        # 初始化白名单列表
        self._refresh_whitelist()
    
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
            修复_module = importlib.import_module('repair')
            SystemRepair = 修复_module.SystemRepair
            from reports import ReportGenerator
            from history import ScanHistory
            
            self.scanner = SilverFoxScanner(verbose=True)
            self.cleaner = SilverFoxCleaner(verbose=True)
            self.repairer = SystemRepair(verbose=True)
            self.report_gen = ReportGenerator(verbose=True)
            self.history = ScanHistory()
            
            self.log("模块初始化成功", "success")
            self.update_status("就绪")
            
            # 加载历史记录
            self._refresh_history()
            
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
    
    # ========== 右键菜单功能 ==========
    
    def _show_context_menu(self, event):
        """显示右键菜单"""
        # 选中右键所在的行
        item = self.result_tree.identify_row(event.y)
        if item:
            if item not in self.result_tree.selection():
                self.result_tree.selection_set(item)
            self.context_menu.tk_popup(event.x_root, event.y_root)
    
    def _on_double_click(self, event):
        """双击打开文件所在位置"""
        self._open_file_location()
    
    def _get_selected_paths(self):
        """获取选中项的路径列表"""
        paths = []
        for item in self.result_tree.selection():
            values = self.result_tree.item(item, "values")
            if len(values) >= 3:
                paths.append(values[2])  # 路径在第3列
        return paths
    
    def _open_file_location(self):
        """打开文件所在位置"""
        paths = self._get_selected_paths()
        if not paths:
            messagebox.showinfo("提示", "请先选择一个文件")
            return
        
        for path in paths:
            if not path or path == "N/A":
                continue
            
            # 获取目录
            if os.path.isfile(path):
                directory = os.path.dirname(path)
            else:
                directory = path
            
            if not os.path.exists(directory):
                messagebox.showwarning("警告", f"路径不存在: {directory}")
                continue
            
            # 跨平台打开文件管理器
            system = platform.system()
            try:
                if system == "Darwin":  # macOS
                    subprocess.run(["open", directory])
                elif system == "Windows":
                    # Windows: 如果是文件，选中它；如果是目录，打开目录
                    if os.path.isfile(path):
                        subprocess.run(["explorer", "/select,", path])
                    else:
                        subprocess.run(["explorer", directory])
                else:  # Linux
                    subprocess.run(["xdg-open", directory])
            except Exception as e:
                messagebox.showerror("错误", f"打开文件位置失败: {e}")
    
    def _copy_file_path(self):
        """复制文件路径"""
        paths = self._get_selected_paths()
        if not paths:
            messagebox.showinfo("提示", "请先选择一个文件")
            return
        
        text = "\n".join(paths)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.log(f"已复制 {len(paths)} 个文件路径到剪贴板", "success")
    
    def _copy_full_path(self):
        """复制完整路径（包含类型和详情）"""
        paths = []
        for item in self.result_tree.selection():
            values = self.result_tree.item(item, "values")
            if len(values) >= 4:
                paths.append(f"[{values[0]}] {values[2]} - {values[3]}")
        
        if not paths:
            messagebox.showinfo("提示", "请先选择一项")
            return
        
        text = "\n".join(paths)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.log(f"已复制 {len(paths)} 条完整信息到剪贴板", "success")
    
    def _add_to_whitelist(self):
        """添加到白名单"""
        paths = self._get_selected_paths()
        if not paths:
            messagebox.showinfo("提示", "请先选择要加入白名单的文件")
            return
        
        # 确认对话框
        count = len(paths)
        confirm = messagebox.askyesno("确认", f"确定要将 {count} 个项目添加到白名单吗？\n\n添加后扫描时将忽略这些文件。")
        if not confirm:
            return
        
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for path in paths:
            if path and path != "N/A" and path not in [item["path"] for item in self.whitelist]:
                self.whitelist.append({
                    "path": path,
                    "added_time": now,
                    "note": "手动添加"
                })
                self.log(f"已添加到白名单: {path}", "success")
        
        self._save_whitelist()
        self._refresh_whitelist()
        messagebox.showinfo("完成", f"已添加 {count} 个项目到白名单")
    
    def _delete_file(self):
        """删除文件"""
        paths = self._get_selected_paths()
        if not paths:
            messagebox.showinfo("提示", "请先选择要删除的文件")
            return
        
        # 确认对话框
        count = len(paths)
        confirm = messagebox.askyesno("确认删除", 
                                       f"确定要删除 {count} 个文件吗？\n\n"
                                       "⚠️ 此操作不可恢复！\n"
                                       "建议先备份重要文件。",
                                       icon=messagebox.WARNING)
        if not confirm:
            return
        
        deleted = 0
        for path in paths:
            if not path or path == "N/A":
                continue
            try:
                if os.path.exists(path):
                    if os.path.isfile(path):
                        os.remove(path)
                        deleted += 1
                        self.log(f"已删除: {path}", "success")
                    elif os.path.isdir(path):
                        import shutil
                        shutil.rmtree(path)
                        deleted += 1
                        self.log(f"已删除目录: {path}", "success")
                else:
                    self.log(f"文件不存在: {path}", "warning")
            except PermissionError:
                self.log(f"删除失败（权限不足）: {path}", "error")
            except Exception as e:
                self.log(f"删除失败: {path} - {e}", "error")
        
        messagebox.showinfo("完成", f"成功删除 {deleted}/{count} 个文件")
    
    def _reveal_in_explorer(self):
        """在资源管理器中选择文件"""
        self._open_file_location()
    
    def _view_details(self):
        """查看详细信息"""
        paths = self._get_selected_paths()
        if not paths:
            messagebox.showinfo("提示", "请先选择一项")
            return
        
        detail_text = ""
        for item in self.result_tree.selection():
            values = self.result_tree.item(item, "values")
            if len(values) >= 4:
                path = values[2]
                detail_text += f"=== 文件详情 ===\n"
                detail_text += f"类型: {values[0]}\n"
                detail_text += f"严重性: {values[1]}\n"
                detail_text += f"路径: {values[2]}\n"
                detail_text += f"详情: {values[3]}\n"
                
                if path and path != "N/A" and os.path.exists(path):
                    try:
                        stat = os.stat(path)
                        from datetime import datetime
                        detail_text += f"文件大小: {stat.st_size} 字节\n"
                        detail_text += f"修改时间: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}\n"
                        detail_text += f"创建时间: {datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}\n"
                        detail_text += f"权限: {oct(stat.st_mode)[-3:]}\n"
                    except:
                        detail_text += "（无法获取文件详细信息）\n"
                else:
                    detail_text += "（文件不存在或路径无效）\n"
                
                detail_text += "\n"
        
        # 显示详情窗口
        detail_window = tk.Toplevel(self.root)
        detail_window.title("文件详细信息")
        detail_window.geometry("500x400")
        
        text_widget = scrolledtext.ScrolledText(detail_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text_widget.insert(tk.END, detail_text)
        text_widget.config(state=tk.DISABLED)
    
    def _export_selected(self):
        """导出选中项"""
        items = []
        for item in self.result_tree.selection():
            values = self.result_tree.item(item, "values")
            if len(values) >= 4:
                items.append({
                    "type": values[0],
                    "severity": values[1],
                    "path": values[2],
                    "detail": values[3]
                })
        
        if not items:
            messagebox.showinfo("提示", "请先选择要导出的项")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("文本文件", "*.txt")],
            title="导出扫描结果"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(items, f, ensure_ascii=False, indent=2)
                self.log(f"已导出 {len(items)} 条记录到: {file_path}", "success")
                messagebox.showinfo("完成", f"已导出到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {e}")
    
    def _export_all(self):
        """导出全部"""
        # 选中所有项
        all_items = self.result_tree.get_children()
        self.result_tree.selection_set(all_items)
        self._export_selected()
    
    # ========== 历史记录功能 ==========
    
    def _refresh_history(self):
        """刷新历史记录"""
        if not self.history:
            return
        
        # 清空列表
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # 获取筛选条件
        filter_text = self.history_filter.get()
        action_filter = None
        if filter_text == "扫描":
            action_filter = "scan"
        elif filter_text == "清理":
            action_filter = "clean"
        elif filter_text == "修复":
            action_filter = "repair"
        elif filter_text == "完整处理":
            action_filter = "full"
        
        # 获取记录
        records = self.history.get_records(limit=50, action_type=action_filter)
        
        # 填充列表
        for record in records:
            time_str = self.history.format_timestamp(record.get("timestamp", ""))
            action_name = self.history.get_action_type_name(record.get("action_type", ""))
            count = record.get("result_count", 0)
            summary = record.get("summary", "")
            
            self.history_tree.insert("", tk.END, 
                                      values=(time_str, action_name, f"{count} 项", summary),
                                      iid=str(record.get("id", "")))
        
        # 更新统计
        stats = self.history.get_statistics()
        self.history_stats_label.config(
            text=f"共 {stats['total_records']} 条记录 | "
                 f"扫描 {stats['scan_count']} | 清理 {stats['clean_count']} | "
                 f"修复 {stats['repair_count']} | 完整处理 {stats['full_count']}"
        )
    
    def _show_history_context_menu(self, event):
        """显示历史记录右键菜单"""
        item = self.history_tree.identify_row(event.y)
        if item:
            if item not in self.history_tree.selection():
                self.history_tree.selection_set(item)
            self.history_context_menu.tk_popup(event.x_root, event.y_root)
    
    def _view_history_detail(self, event):
        """双击查看历史记录详情"""
        self._view_history_detail_menu()
    
    def _view_history_detail_menu(self):
        """查看历史记录详情"""
        selection = self.history_tree.selection()
        if not selection:
            return
        
        record_id = int(selection[0])
        record = self.history.get_record_by_id(record_id)
        
        if not record:
            messagebox.showinfo("提示", "未找到记录详情")
            return
        
        # 显示详情
        self.history_detail_text.config(state=tk.NORMAL)
        self.history_detail_text.delete(1.0, tk.END)
        
        detail = f"时间: {self.history.format_timestamp(record.get('timestamp', ''))}\n"
        detail += f"操作类型: {self.history.get_action_type_name(record.get('action_type', ''))}\n"
        detail += f"发现威胁数: {record.get('result_count', 0)}\n"
        detail += f"摘要: {record.get('summary', '无')}\n"
        detail += f"\n{'='*50}\n详细结果:\n{'='*50}\n\n"
        
        results = record.get("results", [])
        if results:
            for i, r in enumerate(results, 1):
                detail += f"{i}. [{r.get('type', '?')}] {r.get('path', 'N/A')}\n"
                detail += f"   严重性: {r.get('severity', 'N/A')} | 详情: {r.get('detail', 'N/A')}\n\n"
        
        if record.get("truncated"):
            detail += "\n（仅显示前50条结果，完整结果请查看报告文件）\n"
        
        self.history_detail_text.insert(tk.END, detail)
        self.history_detail_text.config(state=tk.DISABLED)
    
    def _replay_history(self):
        """重新执行历史扫描"""
        messagebox.showinfo("提示", "将根据历史记录重新执行扫描...")
        self.notebook.select(0)  # 切换到扫描标签页
        self.start_scan()
    
    def _delete_history_record(self):
        """删除历史记录"""
        selection = self.history_tree.selection()
        if not selection:
            return
        
        confirm = messagebox.askyesno("确认", "确定要删除这条历史记录吗？")
        if not confirm:
            return
        
        record_id = int(selection[0])
        self.history.delete_record(record_id)
        self._refresh_history()
        self.log("已删除历史记录", "info")
    
    def _clear_history(self):
        """清空所有历史记录"""
        confirm = messagebox.askyesno("确认", "确定要清空所有历史记录吗？\n\n此操作不可恢复！")
        if not confirm:
            return
        
        self.history.clear_history()
        self._refresh_history()
        self.log("已清空所有历史记录", "info")
    
    # ========== 白名单功能 ==========
    
    def _refresh_whitelist(self):
        """刷新白名单列表"""
        for item in self.whitelist_tree.get_children():
            self.whitelist_tree.delete(item)
        
        for i, item in enumerate(self.whitelist, 1):
            self.whitelist_tree.insert("", tk.END,
                                       values=(i, item.get("path", ""), 
                                              item.get("added_time", ""),
                                              item.get("note", "")))
    
    def _add_whitelist_item(self):
        """添加白名单项"""
        # 让用户选择文件或输入路径
        path = filedialog.askopenfilename(title="选择要加入白名单的文件")
        if not path:
            # 尝试输入目录
            path = filedialog.askdirectory(title="选择要加入白名单的目录")
        
        if path:
            from datetime import datetime
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 检查是否已存在
            if path in [item["path"] for item in self.whitelist]:
                messagebox.showinfo("提示", "该路径已在白名单中")
                return
            
            note = simpledialog.askstring("备注", "请输入备注（可选）:", initialvalue="手动添加")
            
            self.whitelist.append({
                "path": path,
                "added_time": now,
                "note": note or "手动添加"
            })
            
            self._save_whitelist()
            self._refresh_whitelist()
            self.log(f"已添加到白名单: {path}", "success")
    
    def _remove_whitelist_item(self):
        """移除白名单项"""
        selection = self.whitelist_tree.selection()
        if not selection:
            messagebox.showinfo("提示", "请先选择要移除的项")
            return
        
        confirm = messagebox.askyesno("确认", "确定要移除选中的白名单项吗？")
        if not confirm:
            return
        
        for item_id in selection:
            values = self.whitelist_tree.item(item_id, "values")
            path = values[1]  # 路径在第2列
            self.whitelist = [w for w in self.whitelist if w.get("path") != path]
        
        self._save_whitelist()
        self._refresh_whitelist()
        self.log(f"已移除 {len(selection)} 个白名单项", "info")
    
    # ========== 扫描/清除/修复功能 ==========
    
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
        
        thread = threading.Thread(target=self.run_scan)
        thread.daemon = True
        thread.start()
    
    def run_scan(self):
        """执行扫描"""
        try:
            for i in range(101):
                self.root.after(0, self.update_progress, i)
                time.sleep(0.02)
            
            results = self.scanner.scan_all()
            self.root.after(0, self.scan_complete, results)
            
        except Exception as e:
            self.root.after(0, self.scan_error, str(e))
    
    def scan_complete(self, results):
        """扫描完成"""
        self.clear_results()
        
        # 过滤白名单
        filtered_results = []
        for result in results:
            path = result.get('path', '')
            if not self._is_in_whitelist(path):
                filtered_results.append(result)
                self.add_result(
                    result.get('type', 'unknown'),
                    result.get('severity', 'unknown'),
                    result.get('path', 'N/A'),
                    result.get('detail', 'N/A')
                )
        
        # 保存历史记录
        if self.history:
            self.history.add_record("scan", filtered_results, 
                                    f"扫描完成，发现 {len(filtered_results)} 个威胁")
            self._refresh_history()
        
        # 更新统计
        self.threats_label.config(text=f"威胁: {len(filtered_results)}")
        
        # 更新状态
        skipped = len(results) - len(filtered_results)
        msg = f"扫描完成，发现 {len(filtered_results)} 个威胁"
        if skipped > 0:
            msg += f"（已忽略 {skipped} 个白名单项）"
        
        self.log(msg, "success" if len(filtered_results) == 0 else "warning")
        self.update_status("扫描完成")
        self.update_progress(100)
        
        # 启用按钮
        self.scan_btn.config(state=tk.NORMAL)
        if filtered_results:
            self.clean_btn.config(state=tk.NORMAL)
            self.repair_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
    
    def _is_in_whitelist(self, path):
        """检查路径是否在白名单中"""
        if not path:
            return False
        for item in self.whitelist:
            wl_path = item.get("path", "")
            if path == wl_path or path.startswith(wl_path):
                return True
        return False
    
    def scan_error(self, error_msg):
        """扫描出错"""
        self.log(f"扫描出错: {error_msg}", "error")
        self.update_status("扫描失败")
        self.update_progress(0)
        
        self.scan_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
        
        messagebox.showerror("扫描错误", f"扫描过程中出错: {error_msg}")
    
    def start_clean(self):
        """开始清除"""
        self.log("开始清除病毒...", "info")
        self.update_status("清除中...")
        self.update_progress(0)
        
        self.scan_btn.config(state=tk.DISABLED)
        self.clean_btn.config(state=tk.DISABLED)
        self.repair_btn.config(state=tk.DISABLED)
        self.full_btn.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.run_clean)
        thread.daemon = True
        thread.start()
    
    def run_clean(self):
        """执行清除"""
        try:
            for i in range(101):
                self.root.after(0, self.update_progress, i)
                time.sleep(0.02)
            
            results = self.cleaner.clean_all()
            self.root.after(0, self.clean_complete, results)
            
        except Exception as e:
            self.root.after(0, self.clean_error, str(e))
    
    def clean_complete(self, results):
        """清除完成"""
        cleaned_count = sum(1 for r in results if r.get('success', False))
        self.cleaned_label.config(text=f"已清除: {cleaned_count}")
        
        # 保存历史记录
        if self.history:
            self.history.add_record("clean", results, 
                                    f"清除完成，处理了 {len(results)} 个项目")
            self._refresh_history()
        
        self.log(f"清除完成，处理了 {len(results)} 个项目", "success")
        self.update_status("清除完成")
        self.update_progress(100)
        
        self.scan_btn.config(state=tk.NORMAL)
        self.clean_btn.config(state=tk.NORMAL)
        self.repair_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
    
    def clean_error(self, error_msg):
        """清除出错"""
        self.log(f"清除出错: {error_msg}", "error")
        self.update_status("清除失败")
        self.update_progress(0)
        
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
        
        self.scan_btn.config(state=tk.DISABLED)
        self.clean_btn.config(state=tk.DISABLED)
        self.repair_btn.config(state=tk.DISABLED)
        self.full_btn.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.run_repair)
        thread.daemon = True
        thread.start()
    
    def run_repair(self):
        """执行修复"""
        try:
            for i in range(101):
                self.root.after(0, self.update_progress, i)
                time.sleep(0.02)
            
            results = self.repairer.repair_all()
            self.root.after(0, self.repair_complete, results)
            
        except Exception as e:
            self.root.after(0, self.repair_error, str(e))
    
    def repair_complete(self, results):
        """修复完成"""
        repaired_count = sum(1 for r in results if r.get('success', False))
        self.repaired_label.config(text=f"已修复: {repaired_count}")
        
        # 保存历史记录
        if self.history:
            self.history.add_record("repair", results, 
                                    f"修复完成，处理了 {len(results)} 个设置")
            self._refresh_history()
        
        self.log(f"修复完成，处理了 {len(results)} 个设置", "success")
        self.update_status("修复完成")
        self.update_progress(100)
        
        self.scan_btn.config(state=tk.NORMAL)
        self.clean_btn.config(state=tk.NORMAL)
        self.repair_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
    
    def repair_error(self, error_msg):
        """修复出错"""
        self.log(f"修复出错: {error_msg}", "error")
        self.update_status("修复失败")
        self.update_progress(0)
        
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
        
        self.scan_btn.config(state=tk.DISABLED)
        self.clean_btn.config(state=tk.DISABLED)
        self.repair_btn.config(state=tk.DISABLED)
        self.full_btn.config(state=tk.DISABLED)
        
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
            
            self.root.after(0, self.full_complete, scan_results, clean_results, repair_results)
            
        except Exception as e:
            self.root.after(0, self.full_error, str(e))
    
    def full_complete(self, scan_results, clean_results, repair_results):
        """完整处理完成"""
        self.clear_results()
        
        for result in scan_results:
            self.add_result(
                result.get('type', 'unknown'),
                result.get('severity', 'unknown'),
                result.get('path', 'N/A'),
                result.get('detail', 'N/A')
            )
        
        self.threats_label.config(text=f"威胁: {len(scan_results)}")
        cleaned_count = sum(1 for r in clean_results if r.get('success', False))
        self.cleaned_label.config(text=f"已清除: {cleaned_count}")
        repaired_count = sum(1 for r in repair_results if r.get('success', False))
        self.repaired_label.config(text=f"已修复: {repaired_count}")
        
        # 保存历史记录
        if self.history:
            all_results = scan_results + clean_results + repair_results
            self.history.add_record("full", all_results, 
                                    f"完整处理完成 - 扫描{len(scan_results)}项, 清除{cleaned_count}项, 修复{repaired_count}项")
            self._refresh_history()
        
        self.log("完整处理完成！", "success")
        self.update_status("完整处理完成")
        self.update_progress(100)
        
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
