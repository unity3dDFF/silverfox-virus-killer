"""Running process scanner with correlated evidence."""

from __future__ import annotations

import os

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from ioc import MaliciousHashes, MaliciousProcesses
from scanner.file_scanner import FileScanner


class ProcessScanner:
    SCRIPT_HOSTS = {"powershell.exe", "pwsh.exe", "wscript.exe", "cscript.exe", "mshta.exe"}

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.malicious_processes = MaliciousProcesses()
        self.malicious_hashes = MaliciousHashes()
        self.file_hasher = FileScanner(verbose=verbose, scan_paths=[])
        self._hash_cache = {}

    def scan(self):
        if not PSUTIL_AVAILABLE:
            return []
        results = []
        for proc in psutil.process_iter(["pid", "name", "exe", "cmdline", "create_time"]):
            try:
                result = self._classify(proc)
                if result:
                    results.append(result)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, OSError):
                continue
        return results

    def _classify(self, proc):
        info = proc.info
        name = (info.get("name") or "").lower()
        path = info.get("exe") or ""
        cmdline = " ".join(info.get("cmdline") or [])

        if path not in self._hash_cache:
            self._hash_cache[path] = self.file_hasher.calculate_file_hashes(path) if path else {}
        hashes = self._hash_cache[path]
        matched = self.file_hasher.match_malicious_hash(hashes)
        if matched:
            return self._result(
                info, "critical", "confirmed", "known_process_hash",
                f"运行中进程命中已知恶意{matched[0].upper()}哈希: {matched[1]}", True,
                sha256=hashes.get("sha256"),
            )

        known_names = {item.lower() for item in self.malicious_processes.get_process_names()}
        if name in known_names:
            return self._result(
                info, "medium", "medium", "known_process_name",
                f"进程名与已知 IOC 相同，需结合路径/签名复核: {name}", False,
                sha256=hashes.get("sha256"),
            )

        if self.is_suspicious_process(proc):
            return self._result(
                info, "low", "low", "script_host_in_user_path",
                "脚本宿主或可执行文件从用户临时位置运行（仅线索）", False,
                sha256=hashes.get("sha256"),
            )
        return None

    @staticmethod
    def _result(info, severity, confidence, detector, detail, remediable, sha256=None):
        return {
            "type": "process", "severity": severity, "confidence": confidence,
            "pid": info.get("pid"), "name": info.get("name"), "path": info.get("exe"),
            "cmdline": info.get("cmdline"), "create_time": info.get("create_time"),
            "sha256": sha256, "detail": detail, "detector": detector,
            "action": "recommend_terminate" if remediable else "recommend_investigate",
            "remediable": remediable,
        }

    def is_suspicious_process(self, proc):
        info = proc.info
        name = (info.get("name") or "").lower()
        path = os.path.normcase(info.get("exe") or "")
        cmdline = " ".join(info.get("cmdline") or []).lower()
        user_roots = [
            os.environ.get("TEMP"), os.environ.get("TMP"), os.environ.get("APPDATA"),
            os.environ.get("LOCALAPPDATA"), str(os.path.expanduser("~/Downloads")),
        ]
        in_user_location = any(
            path.startswith(os.path.normcase(os.path.abspath(root)) + os.sep)
            for root in user_roots if root
        )
        return in_user_location and (name in self.SCRIPT_HOSTS or any(
            token in cmdline for token in ("-encodedcommand", "frombase64string", "downloadstring(")
        ))

    def is_malicious_process(self, proc):
        result = self._classify(proc)
        return bool(result and result.get("confidence") == "confirmed")

    def get_process_by_name(self, name):
        if not PSUTIL_AVAILABLE:
            return []
        return [p for p in psutil.process_iter(["pid", "name", "exe", "cmdline"])
                if p.info.get("name") == name]

    def get_process_by_pid(self, pid):
        try:
            return psutil.Process(pid) if PSUTIL_AVAILABLE else None
        except psutil.NoSuchProcess:
            return None

    def is_process_running(self, name):
        return bool(self.get_process_by_name(name))
