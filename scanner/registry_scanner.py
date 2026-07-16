"""Windows persistence scanner with registry location and value evidence."""

from __future__ import annotations

import os
import re
import sys

from ioc import MaliciousRegistryKeys
from scanner.file_scanner import FileScanner

if sys.platform == "win32":
    import winreg
else:
    winreg = None


class RegistryScanner:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.malicious_keys = MaliciousRegistryKeys()
        self.file_hasher = FileScanner(verbose=verbose, scan_paths=[])
        if winreg:
            self.registry_paths = [
                (winreg.HKEY_CURRENT_USER, "HKEY_CURRENT_USER", r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_CURRENT_USER, "HKEY_CURRENT_USER", r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
                (winreg.HKEY_LOCAL_MACHINE, "HKEY_LOCAL_MACHINE", r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE, "HKEY_LOCAL_MACHINE", r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
                (winreg.HKEY_LOCAL_MACHINE, "HKEY_LOCAL_MACHINE", r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows"),
            ]
        else:
            self.registry_paths = []

    def scan(self):
        if not winreg:
            return []
        results = []
        for hive, hive_name, key_path in self.registry_paths:
            results.extend(self.scan_registry_key(hive, key_path, hive_name))
        return results

    def scan_registry_key(self, hive, key_path, hive_name=None):
        hive_name = hive_name or self._hive_name(hive)
        results = []
        access_modes = [winreg.KEY_READ]
        if hasattr(winreg, "KEY_WOW64_64KEY"):
            access_modes = [winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
                            winreg.KEY_READ | winreg.KEY_WOW64_32KEY]
        visited = set()
        for access in access_modes:
            try:
                with winreg.OpenKey(hive, key_path, 0, access) as key:
                    index = 0
                    while True:
                        try:
                            name, value, value_type = winreg.EnumValue(key, index)
                            index += 1
                        except OSError:
                            break
                        marker = (name, str(value))
                        if marker in visited:
                            continue
                        visited.add(marker)
                        result = self._classify_value(hive_name, key_path, name, value, value_type)
                        if result:
                            results.append(result)
            except OSError as exc:
                if self.verbose and getattr(exc, "winerror", None) not in {2, 5}:
                    print(f"无法访问注册表键 {hive_name}\\{key_path}: {exc}")
        return results

    def _classify_value(self, hive_name, key_path, name, value, value_type):
        text = str(value)
        target = self._extract_target(text)
        hashes = self.file_hasher.calculate_file_hashes(target) if target and os.path.isfile(target) else {}
        matched = self.file_hasher.match_malicious_hash(hashes)
        base = {
            "type": "registry", "hive": hive_name, "key_path": key_path,
            "value_name": name, "value": value, "value_type": value_type,
            "path": f"{hive_name}\\{key_path}\\{name}",
        }
        if matched:
            return {**base, "severity": "critical", "confidence": "confirmed",
                    "detector": "registry_target_known_hash", "remediable": True,
                    "detail": f"启动项指向已知恶意{matched[0].upper()}哈希文件: {target}",
                    "action": "recommend_delete"}

        full_key = f"{hive_name}\\{key_path}"
        known_name = self.malicious_keys.is_malicious(full_key, name)
        suspicious = self.is_suspicious_value(name, text)
        if known_name or suspicious:
            reason = "值名称与已知 IOC 相同" if known_name else "命令或路径具有高风险启动特征"
            return {**base, "severity": "medium", "confidence": "medium",
                    "detector": "suspicious_autorun", "remediable": False,
                    "detail": f"{reason}，需人工复核: {name}",
                    "action": "recommend_investigate"}
        return None

    @staticmethod
    def _extract_target(value):
        expanded = os.path.expandvars(str(value)).strip()
        match = re.match(r'^\s*["\']([^"\']+)["\']|^\s*([^\s]+)', expanded)
        return (match.group(1) or match.group(2)) if match else None

    def is_malicious_value(self, name, value):
        return name in self.malicious_keys.get_value_names()

    @staticmethod
    def is_suspicious_value(name, value):
        lowered = str(value).lower()
        command_patterns = ("mshta", "wscript", "cscript", "powershell", "rundll32")
        encoded_patterns = ("-encodedcommand", "frombase64string", "downloadstring(")
        user_path = any(token in lowered for token in ("%temp%", "\\appdata\\", "\\downloads\\"))
        return any(item in lowered for item in encoded_patterns) or (
            user_path and any(item in lowered for item in command_patterns)
        )

    @staticmethod
    def _hive_name(hive):
        mapping = {
            winreg.HKEY_CURRENT_USER: "HKEY_CURRENT_USER",
            winreg.HKEY_LOCAL_MACHINE: "HKEY_LOCAL_MACHINE",
        }
        return mapping.get(hive, str(hive))
