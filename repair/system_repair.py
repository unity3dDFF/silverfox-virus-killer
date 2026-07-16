"""Conservative Windows security repair operations.

The previous implementation reset UAC, Winsock and system services wholesale.
This version limits mutations to enabling built-in protections, flushing DNS,
and removing exact known IOC host entries with a backup. WDAC is audit-only.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from ioc import MaliciousDomains
from quarantine import default_data_dir


class SystemRepair:
    def __init__(self, verbose=False):
        self.verbose = verbose

    @staticmethod
    def _result(kind, action, detail, success, **extra):
        return {"type": kind, "action": action, "detail": detail,
                "success": success, **extra}

    def _run(self, args, timeout=60):
        return subprocess.run(args, capture_output=True, text=True,
                              timeout=timeout, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

    def repair_all(self, progress_callback=None):
        if sys.platform != "win32":
            return [self._result("system", "skipped", "系统修复仅支持 Windows", False, skipped=True)]
        operations = [
            ("正在启用 Windows 防火墙…", self.repair_firewall_settings),
            ("正在检查 Defender 实时保护…", self.repair_defender_settings),
            ("正在刷新 DNS 缓存…", self.repair_dns_settings),
            ("正在核验 hosts 文件…", self.repair_hosts_file),
            ("正在审计 WDAC 策略…", self.inspect_wdac_policies),
        ]
        results = []
        for index, (message, operation) in enumerate(operations, 1):
            if progress_callback:
                progress_callback(index - 1, len(operations), message)
            results.append(operation())
            if progress_callback:
                progress_callback(index, len(operations), results[-1].get("detail", message))
        return results

    def repair_firewall_settings(self):
        try:
            result = self._run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"])
            if result.returncode == 0:
                return self._result("firewall", "enabled", "已启用 Windows 防火墙全部配置文件", True)
            return self._result("firewall", "failed", (result.stderr or result.stdout).strip(), False)
        except Exception as exc:
            return self._result("firewall", "error", f"启用防火墙失败: {exc}", False)

    def repair_defender_settings(self):
        command = [
            "powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
            "Set-MpPreference -DisableRealtimeMonitoring $false -ErrorAction Stop",
        ]
        try:
            result = self._run(command)
            if result.returncode == 0:
                return self._result("security", "enabled", "已请求启用 Microsoft Defender 实时保护", True)
            return self._result("security", "failed", (result.stderr or result.stdout).strip(), False)
        except Exception as exc:
            return self._result("security", "error", f"启用 Defender 失败: {exc}", False)

    def repair_dns_settings(self):
        try:
            result = self._run(["ipconfig", "/flushdns"])
            if result.returncode == 0:
                return self._result("network", "flushed", "已刷新 DNS 缓存", True)
            return self._result("network", "failed", (result.stderr or result.stdout).strip(), False)
        except Exception as exc:
            return self._result("network", "error", f"刷新 DNS 缓存失败: {exc}", False)

    def repair_hosts_file(self):
        hosts_path = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32/drivers/etc/hosts"
        try:
            if not hosts_path.exists():
                return self._result("network", "skipped", "hosts 文件不存在", False, skipped=True)
            raw = hosts_path.read_text(encoding="utf-8", errors="surrogateescape")
            domains = MaliciousDomains()
            kept, removed = [], []
            for line in raw.splitlines(keepends=True):
                content = line.split("#", 1)[0].strip()
                parts = content.split()
                hostnames = parts[1:] if len(parts) > 1 else []
                if any(domains.is_malicious(host) for host in hostnames):
                    removed.append(line.rstrip())
                else:
                    kept.append(line)
            if not removed:
                return self._result("network", "checked", "hosts 文件未发现已知恶意域名", True)
            backup_dir = default_data_dir() / "Backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup = backup_dir / f"hosts-{datetime.now():%Y%m%d-%H%M%S}.bak"
            shutil.copy2(hosts_path, backup)
            hosts_path.write_text("".join(kept), encoding="utf-8", errors="surrogateescape")
            return self._result("network", "repaired",
                                f"已备份 hosts 并移除 {len(removed)} 条 IOC 记录", True,
                                backup=str(backup))
        except Exception as exc:
            return self._result("network", "error", f"修复 hosts 文件失败: {exc}", False)

    def inspect_wdac_policies(self):
        """Report WDAC policy presence; never delete enterprise policies automatically."""
        policy_paths = [
            Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32/CodeIntegrity/SiPolicy.p7b",
            Path(os.environ.get("SystemDrive", "C:")) / "EFI/Microsoft/Boot/SiPolicy.p7b",
        ]
        present = [str(path) for path in policy_paths if path.exists()]
        detail = "未发现传统 SiPolicy.p7b 文件"
        if present:
            detail = "检测到 WDAC 策略文件；可能是企业合法策略，未自动删除: " + ", ".join(present)
        return self._result("wdac", "audit_only", detail, True, paths=present)

    # Compatibility entry points used by older callers.
    def repair_system_settings(self):
        return self.repair_all()

    def repair_security_settings(self):
        return [self.repair_firewall_settings(), self.repair_defender_settings()]

    def repair_network_settings(self):
        return [self.repair_dns_settings(), self.repair_hosts_file()]

    def repair_startup_items(self):
        return [self._result("startup", "audit_only", "启动项由扫描器检测，不执行盲目清理", True)]
