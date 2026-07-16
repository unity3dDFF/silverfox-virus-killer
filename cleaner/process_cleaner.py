"""Conservative process remediation."""

from __future__ import annotations

import os

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False


class ProcessCleaner:
    PROTECTED_NAMES = {
        "system", "registry", "smss.exe", "csrss.exe", "wininit.exe",
        "services.exe", "lsass.exe", "winlogon.exe", "svchost.exe",
        "explorer.exe", "dwm.exe",
    }

    def __init__(self, verbose=False):
        self.verbose = verbose

    def clean_process(self, threat_info):
        if not PSUTIL_AVAILABLE:
            return self._skipped("psutil未安装，无法终止进程")
        if not threat_info.get("remediable") or threat_info.get("confidence") != "confirmed":
            return self._skipped("只有已确认哈希命中的进程才允许自动终止")
        pid = threat_info.get("pid")
        if not pid or pid in {0, 4, os.getpid()}:
            return self._skipped(f"拒绝终止受保护或当前进程 PID: {pid}")
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            if name.lower() in self.PROTECTED_NAMES:
                return self._skipped(f"拒绝终止 Windows 核心进程: {name}")
            expected_path = os.path.normcase(threat_info.get("path") or "")
            actual_path = os.path.normcase(proc.exe() or "")
            expected_created = threat_info.get("create_time")
            if expected_path and expected_path != actual_path:
                return self._skipped("PID 已复用或进程路径发生变化")
            if expected_created and abs(proc.create_time() - float(expected_created)) > 0.01:
                return self._skipped("PID 已复用，创建时间不一致")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except psutil.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)
            return {
                "type": "process", "action": "terminated", "pid": pid,
                "name": name, "path": actual_path,
                "detail": f"已终止确认恶意进程: {name} (PID: {pid})", "success": True,
            }
        except psutil.NoSuchProcess:
            return self._skipped(f"进程 {pid} 已退出")
        except Exception as exc:
            return {
                "type": "process", "action": "error", "pid": pid,
                "detail": f"终止进程失败: {exc}", "success": False,
            }

    @staticmethod
    def _skipped(detail):
        return {"type": "process", "action": "skipped", "detail": detail,
                "success": False, "skipped": True}

    def clean_all(self):
        return [self._skipped("必须先扫描，并根据已确认的扫描结果处理进程")]

    def terminate_process(self, proc):
        return bool(self.clean_process({
            "pid": proc.pid, "path": proc.exe(), "create_time": proc.create_time(),
            "confidence": "confirmed", "remediable": True,
        }).get("success"))
