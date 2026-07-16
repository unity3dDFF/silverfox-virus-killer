"""Safe file remediation: quarantine first, never heuristic deletion."""

from __future__ import annotations

import os

from quarantine import QuarantineManager


class FileCleaner:
    def __init__(self, verbose=False, quarantine_manager=None):
        self.verbose = verbose
        self.quarantine_manager = quarantine_manager or QuarantineManager()

    def clean_file(self, threat_info):
        file_path = threat_info.get("path")
        if not file_path:
            return self._skipped("未指定文件路径")
        if not threat_info.get("remediable", False):
            return self._skipped(f"低置信或启发式结果不自动处理: {file_path}", file_path)
        if threat_info.get("confidence") != "confirmed":
            return self._skipped(f"仅允许自动隔离已确认 IOC: {file_path}", file_path)
        if not os.path.isfile(file_path):
            return self._skipped(f"文件不存在: {file_path}", file_path)

        try:
            entry = self.quarantine_manager.quarantine(
                file_path, reason=threat_info.get("detail", "已确认 IOC")
            )
            return {
                "type": "file",
                "action": "quarantined",
                "path": file_path,
                "quarantine_id": entry["id"],
                "sha256": entry["sha256"],
                "detail": f"文件已隔离，可通过 ID 恢复: {entry['id']}",
                "success": True,
            }
        except Exception as exc:
            if self.verbose:
                print(f"隔离文件时出错: {exc}")
            return {
                "type": "file", "action": "error", "path": file_path,
                "detail": f"隔离文件失败: {exc}", "success": False,
            }

    @staticmethod
    def _skipped(detail, path=None):
        result = {
            "type": "file", "action": "skipped", "detail": detail,
            "success": False, "skipped": True,
        }
        if path:
            result["path"] = path
        return result

    def clean_all(self):
        """Unsafe blind cleanup was intentionally removed."""
        return [self._skipped("必须先扫描，并根据扫描结果执行隔离")]

    def restore(self, quarantine_id, overwrite=False):
        return self.quarantine_manager.restore(quarantine_id, overwrite=overwrite)

    def list_quarantine(self):
        return self.quarantine_manager.list()

    def is_malicious_file(self, file_path):
        return False
