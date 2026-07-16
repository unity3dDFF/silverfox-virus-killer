#!/usr/bin/env python3
"""SilverFox Virus Killer command-line entry point for Windows."""

from __future__ import annotations

import argparse
import ctypes
import json
import sys

from cleaner import SilverFoxCleaner
from quarantine import QuarantineManager
from repair import SystemRepair
from reports import ReportGenerator
from scanner import SilverFoxScanner
from scanner.file_scanner import FileScanner
from version import __version__


def is_admin():
    if sys.platform != "win32":
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def build_parser():
    parser = argparse.ArgumentParser(description="银狐病毒检测与保守处置工具")
    parser.add_argument(
        "action",
        choices=["scan", "clean", "repair", "full", "quarantine-list", "restore"],
        help="scan扫描；clean扫描后隔离确认IOC；repair修复安全设置；full完整处理",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    parser.add_argument("--output", "-o", default="report.txt", help="报告输出文件")
    parser.add_argument("--json", action="store_true", help="同时生成 JSON 报告")
    parser.add_argument("--yes", "-y", action="store_true", help="确认执行会修改系统的操作")
    parser.add_argument("--path", action="append", dest="paths", help="额外/自定义文件扫描目录，可重复")
    parser.add_argument("--id", dest="quarantine_id", help="restore 使用的隔离项 ID")
    parser.add_argument("--overwrite", action="store_true", help="恢复时覆盖原位置已有文件")
    return parser


def make_scanner(args):
    scanner = SilverFoxScanner(verbose=args.verbose)
    if args.paths:
        scanner.file_scanner = FileScanner(verbose=args.verbose, scan_paths=args.paths)
    return scanner


def print_scan_summary(results):
    confirmed = sum(item.get("confidence") == "confirmed" for item in results)
    print(f"扫描完成：{len(results)} 条线索，其中 {confirmed} 条为已确认 IOC。")
    for item in results:
        print(f"[{item.get('severity', 'unknown').upper()}] "
              f"[{item.get('confidence', 'unknown')}] {item.get('detail', '')}")
        location = item.get("path") or item.get("remote_address")
        if location:
            print(f"  {location}")


def save_scan_report(results, args):
    reporter = ReportGenerator(verbose=args.verbose)
    reporter.generate_report("scan", results, args.output)
    if args.json:
        reporter.save_report_as_json(results, args.output + ".json")
    print(f"报告已保存到: {args.output}")


def main(argv=None):
    args = build_parser().parse_args(argv)
    print(f"银狐病毒专杀工具 v{__version__} | Windows 保守处置版")
    print(f"管理员权限: {'是' if is_admin() else '否'}")

    quarantine = QuarantineManager()
    if args.action == "quarantine-list":
        entries = quarantine.list()
        print(json.dumps(entries, ensure_ascii=False, indent=2))
        return 0
    if args.action == "restore":
        if not args.quarantine_id:
            print("错误：restore 需要 --id", file=sys.stderr)
            return 2
        if not args.yes:
            print("恢复文件会修改磁盘；请确认后添加 --yes。", file=sys.stderr)
            return 2
        entry = quarantine.restore(args.quarantine_id, overwrite=args.overwrite)
        print(f"已恢复: {entry['original_path']}")
        return 0

    scan_results = []
    clean_results = []
    repair_results = []
    if args.action in {"scan", "clean", "full"}:
        scan_results = make_scanner(args).scan_all()
        print_scan_summary(scan_results)
        if args.action == "scan":
            save_scan_report(scan_results, args)
            return 1 if any(x.get("confidence") == "confirmed" for x in scan_results) else 0

    if args.action in {"clean", "full"}:
        if not args.yes:
            print("未执行处置：文件隔离/终止进程/注册表清理需要 --yes。")
        else:
            clean_results = SilverFoxCleaner(verbose=args.verbose).clean_all(scan_results)
            success = sum(item.get("success", False) for item in clean_results)
            skipped = sum(item.get("skipped", False) for item in clean_results)
            print(f"处置完成：成功 {success}，跳过 {skipped}。")

    if args.action in {"repair", "full"}:
        if not args.yes:
            print("未执行系统修复：启用安全组件等操作需要 --yes。")
        else:
            repair_results = SystemRepair(verbose=args.verbose).repair_all()
            success = sum(item.get("success", False) for item in repair_results)
            print(f"修复完成：{success}/{len(repair_results)} 项成功。")

    reporter = ReportGenerator(verbose=args.verbose)
    if args.action == "clean":
        reporter.generate_full_report(scan_results, clean_results, [], args.output)
    elif args.action == "repair":
        reporter.generate_report("repair", repair_results, args.output)
    else:
        reporter.generate_full_report(scan_results, clean_results, repair_results, args.output)
    if args.json:
        reporter.save_report_as_json({
            "scan": scan_results, "clean": clean_results, "repair": repair_results,
        }, args.output + ".json")
    print(f"报告已保存到: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
