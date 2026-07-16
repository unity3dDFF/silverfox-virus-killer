#!/usr/bin/env python3
"""Modern Tkinter interface for SilverFox Virus Killer."""

from __future__ import annotations

import ctypes
import json
import os
import subprocess
import threading
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk

from cleaner import SilverFoxCleaner
from history import ScanHistory
from quarantine import QuarantineManager, default_data_dir
from repair import SystemRepair
from reports import ReportGenerator
from scanner import SilverFoxScanner
from version import __version__


class SilverFoxKillerGUI:
    BG = "#F3F6FA"
    SURFACE = "#FFFFFF"
    NAVY = "#10243E"
    TEXT = "#1D2939"
    MUTED = "#667085"
    BLUE = "#2563EB"
    BLUE_HOVER = "#1D4ED8"
    GREEN = "#15803D"
    AMBER = "#B45309"
    RED = "#B42318"
    BORDER = "#DCE3EC"

    def __init__(self, root):
        self.root = root
        self.root.title(f"银狐病毒专杀工具 v{__version__}")
        self.root.geometry("1180x760")
        self.root.minsize(980, 660)
        self.root.configure(bg=self.BG)

        self.scanner = SilverFoxScanner(verbose=False)
        self.cleaner = SilverFoxCleaner(verbose=False)
        self.repairer = SystemRepair(verbose=False)
        self.reporter = ReportGenerator(verbose=False)
        self.quarantine = QuarantineManager()
        self.history = ScanHistory()
        self.whitelist_path = default_data_dir() / "whitelist.json"
        self.whitelist = self._load_whitelist()
        self.last_scan_results = []
        self.busy = False

        self._configure_styles()
        self._build_layout()
        self._set_summary(0, 0, 0, "就绪")
        self._log("防护引擎已就绪。扫描不会上传文件，启发式线索不会自动处置。", "info")

    def _configure_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("App.TFrame", background=self.BG)
        style.configure("Card.TFrame", background=self.SURFACE)
        style.configure("Header.TLabel", background=self.NAVY, foreground="white",
                        font=("Microsoft YaHei UI", 20, "bold"))
        style.configure("HeaderSub.TLabel", background=self.NAVY, foreground="#C7D7EA",
                        font=("Microsoft YaHei UI", 9))
        style.configure("CardTitle.TLabel", background=self.SURFACE, foreground=self.MUTED,
                        font=("Microsoft YaHei UI", 9))
        style.configure("CardValue.TLabel", background=self.SURFACE, foreground=self.TEXT,
                        font=("Microsoft YaHei UI", 20, "bold"))
        style.configure("Section.TLabel", background=self.BG, foreground=self.TEXT,
                        font=("Microsoft YaHei UI", 11, "bold"))
        style.configure("Primary.TButton", background=self.BLUE, foreground="white",
                        borderwidth=0, padding=(18, 10), font=("Microsoft YaHei UI", 9, "bold"))
        style.map("Primary.TButton", background=[("active", self.BLUE_HOVER), ("disabled", "#9AB5E8")])
        style.configure("Secondary.TButton", background=self.SURFACE, foreground=self.TEXT,
                        bordercolor=self.BORDER, borderwidth=1, padding=(14, 9),
                        font=("Microsoft YaHei UI", 9))
        style.map("Secondary.TButton", background=[("active", "#EAF0F7")])
        style.configure("Danger.TButton", background="#FEE4E2", foreground=self.RED,
                        borderwidth=0, padding=(14, 9), font=("Microsoft YaHei UI", 9, "bold"))
        style.configure("Treeview", background=self.SURFACE, fieldbackground=self.SURFACE,
                        foreground=self.TEXT, rowheight=31, borderwidth=0,
                        font=("Microsoft YaHei UI", 9))
        style.configure("Treeview.Heading", background="#EAF0F7", foreground=self.TEXT,
                        relief="flat", padding=(8, 8), font=("Microsoft YaHei UI", 9, "bold"))
        style.map("Treeview", background=[("selected", "#DCE9FF")], foreground=[("selected", self.TEXT)])
        style.configure("Scan.Horizontal.TProgressbar", troughcolor="#DCE3EC",
                        background=self.BLUE, borderwidth=0, lightcolor=self.BLUE, darkcolor=self.BLUE)

    def _build_layout(self):
        header = tk.Frame(self.root, bg=self.NAVY, height=92)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        title_box = tk.Frame(header, bg=self.NAVY)
        title_box.pack(side=tk.LEFT, padx=28, pady=17)
        ttk.Label(title_box, text="银狐病毒专杀工具", style="Header.TLabel").pack(anchor=tk.W)
        ttk.Label(title_box, text="Windows 证据分级检测 · 默认隔离 · 支持恢复",
                  style="HeaderSub.TLabel").pack(anchor=tk.W, pady=(3, 0))

        badge_text = "管理员模式" if self._is_admin() else "普通权限"
        badge_color = "#166534" if self._is_admin() else "#92400E"
        tk.Label(header, text=badge_text, bg=badge_color, fg="white",
                 font=("Microsoft YaHei UI", 9, "bold"), padx=12, pady=6).pack(
                     side=tk.RIGHT, padx=(8, 28))
        tk.Label(header, text=f"v{__version__}", bg="#203B5D", fg="#DCE8F5",
                 font=("Segoe UI", 9, "bold"), padx=10, pady=6).pack(side=tk.RIGHT)

        main = ttk.Frame(self.root, style="App.TFrame", padding=(24, 18, 24, 16))
        main.pack(fill=tk.BOTH, expand=True)

        cards = ttk.Frame(main, style="App.TFrame")
        cards.pack(fill=tk.X)
        for column in range(4):
            cards.columnconfigure(column, weight=1, uniform="stats")
        self.summary_labels = {}
        for column, (key, title) in enumerate((
            ("findings", "检测线索"), ("confirmed", "确认 IOC"),
            ("handled", "已处置"), ("state", "当前状态"),
        )):
            card = ttk.Frame(cards, style="Card.TFrame", padding=(18, 13))
            card.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 6,
                                                                 0 if column == 3 else 6))
            ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor=tk.W)
            label = ttk.Label(card, text="0", style="CardValue.TLabel")
            label.pack(anchor=tk.W, pady=(4, 0))
            self.summary_labels[key] = label

        actions = ttk.Frame(main, style="App.TFrame")
        actions.pack(fill=tk.X, pady=(16, 12))
        self.scan_button = ttk.Button(actions, text="开始扫描", style="Primary.TButton",
                                      command=self.start_scan)
        self.scan_button.pack(side=tk.LEFT)
        self.clean_button = ttk.Button(actions, text="隔离确认项", style="Danger.TButton",
                                       command=self.start_clean, state=tk.DISABLED)
        self.clean_button.pack(side=tk.LEFT, padx=8)
        self.repair_button = ttk.Button(actions, text="安全修复", style="Secondary.TButton",
                                        command=self.start_repair)
        self.repair_button.pack(side=tk.LEFT)
        self.full_button = ttk.Button(actions, text="扫描并修复", style="Secondary.TButton",
                                      command=self.start_full)
        self.full_button.pack(side=tk.LEFT, padx=8)
        self.quarantine_button = ttk.Button(actions, text="隔离区", style="Secondary.TButton",
                                            command=self.show_quarantine)
        self.quarantine_button.pack(side=tk.RIGHT)
        self.history_button = ttk.Button(actions, text="历史记录", style="Secondary.TButton",
                                         command=self.show_history)
        self.history_button.pack(side=tk.RIGHT, padx=8)
        self.whitelist_button = ttk.Button(actions, text="白名单", style="Secondary.TButton",
                                           command=self.show_whitelist)
        self.whitelist_button.pack(side=tk.RIGHT)
        self.export_button = ttk.Button(actions, text="导出报告", style="Secondary.TButton",
                                        command=self.export_report, state=tk.DISABLED)
        self.export_button.pack(side=tk.RIGHT, padx=8)

        progress_box = ttk.Frame(main, style="Card.TFrame", padding=(16, 11))
        progress_box.pack(fill=tk.X, pady=(0, 12))
        self.progress_text = ttk.Label(progress_box, text="等待开始", style="CardTitle.TLabel")
        self.progress_text.pack(side=tk.LEFT)
        self.progress_value = ttk.Label(progress_box, text="0%", style="CardTitle.TLabel")
        self.progress_value.pack(side=tk.RIGHT)
        self.progress = ttk.Progressbar(progress_box, style="Scan.Horizontal.TProgressbar",
                                        mode="determinate", maximum=100)
        self.progress.pack(fill=tk.X, pady=(7, 0))

        pane = ttk.Panedwindow(main, orient=tk.VERTICAL)
        pane.pack(fill=tk.BOTH, expand=True)

        findings_card = ttk.Frame(pane, style="Card.TFrame", padding=(0, 0, 0, 0))
        pane.add(findings_card, weight=4)
        columns = ("severity", "confidence", "type", "location", "detail")
        self.tree = ttk.Treeview(findings_card, columns=columns, show="headings")
        headings = {"severity": "风险", "confidence": "置信度", "type": "类型",
                    "location": "位置 / 远端", "detail": "检测依据"}
        widths = {"severity": 72, "confidence": 80, "type": 75,
                  "location": 310, "detail": 470}
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], minwidth=60,
                             stretch=column in {"location", "detail"})
        self.tree.tag_configure("critical", foreground=self.RED)
        self.tree.tag_configure("high", foreground="#C2410C")
        self.tree.tag_configure("medium", foreground=self.AMBER)
        self.tree.tag_configure("low", foreground=self.MUTED)
        self.tree.bind("<Button-3>", self._show_finding_menu)
        self.finding_menu = tk.Menu(self.root, tearoff=0)
        self.finding_menu.add_command(label="复制位置", command=self._copy_selected_location)
        self.finding_menu.add_command(label="在资源管理器中显示", command=self._reveal_selected)
        self.finding_menu.add_separator()
        self.finding_menu.add_command(label="加入白名单", command=self._whitelist_selected)
        scrollbar = ttk.Scrollbar(findings_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        log_card = ttk.Frame(pane, style="Card.TFrame", padding=(12, 8))
        pane.add(log_card, weight=1)
        log_header = ttk.Frame(log_card, style="Card.TFrame")
        log_header.pack(fill=tk.X)
        ttk.Label(log_header, text="运行日志", style="CardTitle.TLabel").pack(side=tk.LEFT)
        ttk.Button(log_header, text="清空", style="Secondary.TButton",
                   command=lambda: self.log_text.delete("1.0", tk.END)).pack(side=tk.RIGHT)
        self.log_text = scrolledtext.ScrolledText(
            log_card, height=6, wrap=tk.WORD, borderwidth=0, bg="#F8FAFC",
            fg=self.TEXT, insertbackground=self.TEXT, font=("Consolas", 9), padx=8, pady=6)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(6, 0))
        self.log_text.tag_configure("info", foreground=self.MUTED)
        self.log_text.tag_configure("success", foreground=self.GREEN)
        self.log_text.tag_configure("warning", foreground=self.AMBER)
        self.log_text.tag_configure("error", foreground=self.RED)

    @staticmethod
    def _is_admin():
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False

    def _load_whitelist(self):
        try:
            data = json.loads(self.whitelist_path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    def _save_whitelist(self):
        self.whitelist_path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.whitelist_path.with_suffix(".tmp")
        temp.write_text(json.dumps(self.whitelist, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(temp, self.whitelist_path)

    def _is_whitelisted(self, path):
        if not path:
            return False
        normalized = os.path.normcase(os.path.abspath(path))
        for entry in self.whitelist:
            allowed = entry.get("path", "")
            if not allowed:
                continue
            allowed = os.path.normcase(os.path.abspath(allowed))
            if normalized == allowed or normalized.startswith(allowed + os.sep):
                return True
        return False

    def _filter_whitelist(self, results):
        return [item for item in results if not self._is_whitelisted(item.get("path"))]

    def _log(self, message, level="info"):
        stamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{stamp}] {message}\n", level)
        self.log_text.see(tk.END)

    def _thread_progress(self, percent, message):
        self.root.after(0, self._apply_progress, percent, message)

    def _apply_progress(self, percent, message):
        value = max(0, min(100, int(percent)))
        self.progress["value"] = value
        self.progress_value.config(text=f"{value}%")
        self.progress_text.config(text=message)
        self.summary_labels["state"].config(text=message[:12])

    def _set_summary(self, findings, confirmed, handled, state):
        self.summary_labels["findings"].config(text=str(findings))
        self.summary_labels["confirmed"].config(text=str(confirmed))
        self.summary_labels["handled"].config(text=str(handled))
        self.summary_labels["state"].config(text=state)

    def _set_busy(self, busy):
        self.busy = busy
        state = tk.DISABLED if busy else tk.NORMAL
        for button in (self.scan_button, self.repair_button, self.full_button,
                       self.quarantine_button, self.history_button, self.whitelist_button):
            button.config(state=state)
        self.clean_button.config(state=tk.DISABLED if busy or not self._confirmed_count() else tk.NORMAL)
        self.export_button.config(state=tk.DISABLED if busy or not self.last_scan_results else tk.NORMAL)

    def _confirmed_count(self):
        return sum(1 for item in self.last_scan_results
                   if item.get("confidence") == "confirmed" and item.get("remediable"))

    def _run_background(self, target):
        self._set_busy(True)
        threading.Thread(target=target, daemon=True).start()

    def _clear_findings(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _render_findings(self, results):
        self._clear_findings()
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        for result in sorted(results, key=lambda x: severity_order.get(x.get("severity"), 9)):
            severity = result.get("severity", "unknown")
            location = result.get("path") or result.get("remote_address", "N/A")
            self.tree.insert("", tk.END, values=(
                severity.upper(), result.get("confidence", "unknown"),
                result.get("type", "unknown"), location, result.get("detail", "")),
                tags=(severity,))

    def start_scan(self):
        self._clear_findings()
        self._apply_progress(0, "正在准备扫描…")
        self._log("开始扫描系统。", "info")

        def worker():
            try:
                results = self.scanner.scan_all(self._thread_progress)
                self.root.after(0, self._scan_complete, results)
            except Exception as exc:
                self.root.after(0, self._operation_error, "扫描失败", str(exc))
        self._run_background(worker)

    def _scan_complete(self, results):
        results = self._filter_whitelist(results)
        self.last_scan_results = results
        confirmed = sum(item.get("confidence") == "confirmed" for item in results)
        self._render_findings(results)
        self._set_summary(len(results), confirmed, 0, "扫描完成")
        self._apply_progress(100, f"扫描完成：{len(results)} 条线索，{confirmed} 条确认 IOC")
        self._log(f"扫描完成：{len(results)} 条线索，{confirmed} 条确认 IOC。",
                  "success" if confirmed == 0 else "warning")
        self.history.add_record("scan", results,
                                f"扫描完成：{len(results)} 条线索，{confirmed} 条确认 IOC")
        self._set_busy(False)

    def start_clean(self):
        count = self._confirmed_count()
        if not count:
            messagebox.showinfo("无需处置", "当前没有可自动处置的确认 IOC。")
            return
        if not messagebox.askyesno("确认处置",
                                   f"将处置 {count} 个确认 IOC。文件会先隔离并支持恢复，是否继续？"):
            return
        self._apply_progress(0, "正在准备处置…")

        def worker():
            try:
                results = self.cleaner.clean_all(
                    self.last_scan_results,
                    lambda current, total, message: self._thread_progress(
                        current / max(total, 1) * 100, message))
                self.root.after(0, self._clean_complete, results)
            except Exception as exc:
                self.root.after(0, self._operation_error, "处置失败", str(exc))
        self._run_background(worker)

    def _clean_complete(self, results):
        handled = sum(item.get("success", False) for item in results)
        self._set_summary(len(self.last_scan_results),
                          sum(x.get("confidence") == "confirmed" for x in self.last_scan_results),
                          handled, "处置完成")
        self._apply_progress(100, f"处置完成：成功 {handled} 项")
        self._log(f"处置完成：成功 {handled} 项；其余低置信线索保持不变。", "success")
        self.history.add_record("clean", results, f"处置完成：成功 {handled} 项")
        self._set_busy(False)

    def start_repair(self):
        if not messagebox.askyesno(
            "确认安全修复",
            "将启用防火墙和 Defender、刷新 DNS、备份后清理 hosts 精确 IOC。WDAC 只审计不删除。继续吗？"):
            return
        self._apply_progress(0, "正在准备安全修复…")

        def worker():
            try:
                results = self.repairer.repair_all(
                    lambda current, total, message: self._thread_progress(
                        current / max(total, 1) * 100, message))
                self.root.after(0, self._repair_complete, results)
            except Exception as exc:
                self.root.after(0, self._operation_error, "修复失败", str(exc))
        self._run_background(worker)

    def _repair_complete(self, results):
        success = sum(item.get("success", False) for item in results)
        self._apply_progress(100, f"安全修复完成：{success}/{len(results)} 项成功")
        self._log(f"安全修复完成：{success}/{len(results)} 项成功。", "success")
        self.history.add_record("repair", results,
                                f"安全修复完成：{success}/{len(results)} 项成功")
        self.summary_labels["state"].config(text="修复完成")
        self._set_busy(False)

    def start_full(self):
        if not messagebox.askyesno(
            "确认扫描并修复",
            "将先扫描，再仅处置确认 IOC，最后执行保守安全修复。是否继续？"):
            return
        self._clear_findings()
        self._apply_progress(0, "正在准备完整处理…")

        def worker():
            try:
                scan_results = self.scanner.scan_all(
                    lambda value, message: self._thread_progress(value * 0.65, message))
                scan_results = self._filter_whitelist(scan_results)
                clean_results = self.cleaner.clean_all(
                    scan_results,
                    lambda current, total, message: self._thread_progress(
                        65 + current / max(total, 1) * 17, message))
                repair_results = self.repairer.repair_all(
                    lambda current, total, message: self._thread_progress(
                        82 + current / max(total, 1) * 18, message))
                self.root.after(0, self._full_complete, scan_results, clean_results, repair_results)
            except Exception as exc:
                self.root.after(0, self._operation_error, "完整处理失败", str(exc))
        self._run_background(worker)

    def _full_complete(self, scan_results, clean_results, repair_results):
        scan_results = self._filter_whitelist(scan_results)
        self.last_scan_results = scan_results
        confirmed = sum(item.get("confidence") == "confirmed" for item in scan_results)
        handled = sum(item.get("success", False) for item in clean_results)
        repaired = sum(item.get("success", False) for item in repair_results)
        self._render_findings(scan_results)
        self._set_summary(len(scan_results), confirmed, handled, "全部完成")
        self._apply_progress(100, f"全部完成：处置 {handled} 项，修复 {repaired} 项")
        self._log(f"完整处理完成：确认 {confirmed}，处置 {handled}，修复 {repaired}。", "success")
        self.history.add_record("full", scan_results + clean_results + repair_results,
                                f"完整处理：确认 {confirmed}，处置 {handled}，修复 {repaired}")
        self._set_busy(False)

    def _operation_error(self, title, detail):
        self._apply_progress(0, title)
        self._log(f"{title}: {detail}", "error")
        self.summary_labels["state"].config(text="发生错误")
        self._set_busy(False)
        messagebox.showerror(title, detail)

    def _selected_location(self):
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0], "values")[3]

    def _show_finding_menu(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        self.tree.selection_set(item)
        self.finding_menu.tk_popup(event.x_root, event.y_root)

    def _copy_selected_location(self):
        location = self._selected_location()
        if location:
            self.root.clipboard_clear()
            self.root.clipboard_append(location)
            self._log(f"已复制位置: {location}", "info")

    def _reveal_selected(self):
        location = self._selected_location()
        if not location or not os.path.exists(location):
            messagebox.showinfo("无法打开", "所选项不是本机现存文件。")
            return
        subprocess.Popen(["explorer.exe", "/select,", os.path.abspath(location)])

    def _whitelist_selected(self):
        location = self._selected_location()
        if location:
            self._add_whitelist_path(location, "从扫描结果添加")

    def _add_whitelist_path(self, path, note="手动添加"):
        path = os.path.abspath(path)
        if any(os.path.normcase(item.get("path", "")) == os.path.normcase(path)
               for item in self.whitelist):
            messagebox.showinfo("白名单", "该路径已在白名单中。")
            return False
        self.whitelist.append({
            "path": path, "added_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "note": note,
        })
        self._save_whitelist()
        self._log(f"已加入白名单: {path}", "success")
        return True

    def show_whitelist(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("白名单管理")
        dialog.geometry("820x430")
        dialog.configure(bg=self.BG)
        dialog.transient(self.root)
        frame = ttk.Frame(dialog, style="App.TFrame", padding=18)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text=f"白名单 · {len(self.whitelist)} 项", style="Section.TLabel").pack(anchor=tk.W)
        tree = ttk.Treeview(frame, columns=("path", "time", "note"), show="headings")
        for column, title, width in (("path", "路径", 440), ("time", "添加时间", 150),
                                     ("note", "备注", 180)):
            tree.heading(column, text=title)
            tree.column(column, width=width, stretch=column == "path")

        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            for index, entry in enumerate(self.whitelist):
                tree.insert("", tk.END, iid=str(index), values=(
                    entry.get("path", ""), entry.get("added_time", ""), entry.get("note", "")))

        def add_file():
            path = filedialog.askopenfilename(title="选择白名单文件", parent=dialog)
            if path:
                note = simpledialog.askstring("备注", "备注（可选）", parent=dialog) or "手动添加"
                if self._add_whitelist_path(path, note):
                    refresh()

        def add_directory():
            path = filedialog.askdirectory(title="选择白名单目录", parent=dialog)
            if path and self._add_whitelist_path(path, "目录白名单"):
                refresh()

        def remove_selected():
            indexes = sorted((int(item) for item in tree.selection()), reverse=True)
            if not indexes:
                return
            for index in indexes:
                self.whitelist.pop(index)
            self._save_whitelist()
            refresh()

        refresh()
        tree.pack(fill=tk.BOTH, expand=True, pady=12)
        ttk.Button(frame, text="移除所选", style="Danger.TButton",
                   command=remove_selected).pack(side=tk.RIGHT)
        ttk.Button(frame, text="添加目录", style="Secondary.TButton",
                   command=add_directory).pack(side=tk.LEFT)
        ttk.Button(frame, text="添加文件", style="Primary.TButton",
                   command=add_file).pack(side=tk.LEFT, padx=8)

    def show_history(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("操作历史")
        dialog.geometry("900x500")
        dialog.configure(bg=self.BG)
        dialog.transient(self.root)
        frame = ttk.Frame(dialog, style="App.TFrame", padding=18)
        frame.pack(fill=tk.BOTH, expand=True)
        records = self.history.get_records(limit=100)
        ttk.Label(frame, text=f"操作历史 · {len(records)} 条", style="Section.TLabel").pack(anchor=tk.W)
        tree = ttk.Treeview(frame, columns=("time", "action", "count", "summary"), show="headings")
        for column, title, width in (("time", "时间", 155), ("action", "操作", 80),
                                     ("count", "结果数", 70), ("summary", "摘要", 520)):
            tree.heading(column, text=title)
            tree.column(column, width=width, stretch=column == "summary")
        record_map = {}
        for record in records:
            iid = str(record.get("id"))
            record_map[iid] = record
            tree.insert("", tk.END, iid=iid, values=(
                self.history.format_timestamp(record.get("timestamp", "")),
                self.history.get_action_type_name(record.get("action_type", "")),
                record.get("result_count", 0), record.get("summary", "")))
        tree.pack(fill=tk.BOTH, expand=True, pady=(12, 8))
        detail = scrolledtext.ScrolledText(frame, height=7, wrap=tk.WORD, borderwidth=0,
                                           bg="#F8FAFC", font=("Microsoft YaHei UI", 9))
        detail.pack(fill=tk.X)

        def show_detail(_event=None):
            selection = tree.selection()
            if not selection:
                return
            record = record_map[selection[0]]
            detail.delete("1.0", tk.END)
            detail.insert(tk.END, json.dumps(record, ensure_ascii=False, indent=2))

        tree.bind("<<TreeviewSelect>>", show_detail)

    def export_report(self):
        if not self.last_scan_results:
            return
        path = filedialog.asksaveasfilename(
            title="导出扫描报告", defaultextension=".txt",
            filetypes=(("文本报告", "*.txt"), ("JSON 报告", "*.json")))
        if not path:
            return
        ok = (self.reporter.save_report_as_json(self.last_scan_results, path)
              if path.lower().endswith(".json")
              else self.reporter.generate_report("scan", self.last_scan_results, path))
        if ok:
            self._log(f"报告已导出: {path}", "success")
            messagebox.showinfo("导出完成", f"报告已保存到：\n{path}")
        else:
            messagebox.showerror("导出失败", "无法写入报告文件。")

    def show_quarantine(self):
        entries = self.quarantine.list()
        dialog = tk.Toplevel(self.root)
        dialog.title("隔离区")
        dialog.geometry("820x430")
        dialog.minsize(680, 360)
        dialog.configure(bg=self.BG)
        dialog.transient(self.root)
        frame = ttk.Frame(dialog, style="App.TFrame", padding=18)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text=f"隔离文件 · {len(entries)} 项", style="Section.TLabel").pack(anchor=tk.W)
        tree = ttk.Treeview(frame, columns=("id", "name", "time", "path"), show="headings")
        for column, title, width in (("id", "恢复 ID", 210), ("name", "文件名", 150),
                                     ("time", "隔离时间", 150), ("path", "原始路径", 300)):
            tree.heading(column, text=title)
            tree.column(column, width=width, stretch=column == "path")
        for entry in entries:
            tree.insert("", tk.END, iid=entry["id"], values=(
                entry["id"], entry.get("original_name", ""),
                entry.get("timestamp", "")[:19].replace("T", " "), entry.get("original_path", "")))
        tree.pack(fill=tk.BOTH, expand=True, pady=12)

        def restore_selected():
            selection = tree.selection()
            if not selection:
                messagebox.showinfo("请选择文件", "请先选择一个隔离文件。", parent=dialog)
                return
            item_id = selection[0]
            if not messagebox.askyesno("确认恢复", "将文件恢复到原位置，是否继续？", parent=dialog):
                return
            try:
                restored = self.quarantine.restore(item_id)
                tree.delete(item_id)
                self._log(f"已恢复隔离文件: {restored['original_path']}", "success")
            except Exception as exc:
                messagebox.showerror("恢复失败", str(exc), parent=dialog)

        ttk.Button(frame, text="恢复所选文件", style="Primary.TButton",
                   command=restore_selected).pack(side=tk.RIGHT)


def main():
    root = tk.Tk()
    SilverFoxKillerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
