"""Backed-up registry value cleanup for confirmed detections only."""

from __future__ import annotations

import json
import sys
from datetime import datetime

from quarantine import default_data_dir

if sys.platform == "win32":
    import winreg
else:
    winreg = None


class RegistryCleaner:
    HIVES = {
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER if winreg else None,
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE if winreg else None,
    }

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.backup_dir = default_data_dir() / "RegistryBackups"

    def clean_registry(self, threat_info):
        if not winreg:
            return self._skipped("注册表清理仅支持 Windows")
        if not threat_info.get("remediable") or threat_info.get("confidence") != "confirmed":
            return self._skipped("只有指向已确认恶意哈希文件的启动项才允许自动清理")
        hive_name = threat_info.get("hive")
        key_path = threat_info.get("key_path")
        value_name = threat_info.get("value_name")
        hive = self.HIVES.get(hive_name)
        if not hive or not key_path or value_name is None:
            return self._skipped("扫描结果缺少完整注册表定位信息")
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            backup = self.backup_dir / f"registry-{datetime.now():%Y%m%d-%H%M%S-%f}.json"
            backup.write_text(json.dumps({
                "hive": hive_name, "key_path": key_path, "value_name": value_name,
                "value": threat_info.get("value"), "value_type": threat_info.get("value_type"),
            }, ensure_ascii=False, indent=2), encoding="utf-8")
            with winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, value_name)
            return {"type": "registry", "action": "deleted", "path": threat_info.get("path"),
                    "backup": str(backup), "detail": f"已备份并删除确认恶意启动项: {value_name}",
                    "success": True}
        except Exception as exc:
            return {"type": "registry", "action": "error", "path": threat_info.get("path"),
                    "detail": f"注册表清理失败: {exc}", "success": False}

    @staticmethod
    def _skipped(detail):
        return {"type": "registry", "action": "skipped", "detail": detail,
                "success": False, "skipped": True}

    def clean_all(self):
        return [self._skipped("必须先扫描，并根据确认结果清理注册表")]

    def registry_value_exists(self, hive, key_path, value_name):
        if not winreg:
            return False
        try:
            with winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ) as key:
                winreg.QueryValueEx(key, value_name)
            return True
        except OSError:
            return False
