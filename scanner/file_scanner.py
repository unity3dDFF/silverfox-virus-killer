"""Targeted file scanner with evidence-aware SilverFox detections."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

from ioc import MaliciousHashes


class FileScanner:
    """Scan common delivery and persistence locations without deleting files."""

    EXECUTABLE_EXTENSIONS = {
        ".exe", ".dll", ".msi", ".scr", ".com", ".bat", ".cmd",
        ".ps1", ".vbs", ".js", ".jse", ".wsf", ".hta", ".lnk",
    }
    LURE_PATTERNS = (
        "开票-目录", "违规-告示", "违规-记录", "金稅", "违纪名单",
        "裁员名单", "补偿方案", "内部调查结果",
    )
    MAX_HASH_SIZE = 512 * 1024 * 1024

    def __init__(self, verbose=False, scan_paths=None):
        self.verbose = verbose
        self.malicious_hashes = MaliciousHashes()
        self.scan_paths = [Path(path) for path in (scan_paths or self._default_paths())]

    @staticmethod
    def _default_paths():
        values = [
            os.environ.get("TEMP"),
            os.environ.get("TMP"),
            os.environ.get("APPDATA"),
            os.environ.get("LOCALAPPDATA"),
            os.environ.get("PUBLIC"),
            str(Path.home() / "Downloads"),
            str(Path.home() / "Desktop"),
        ]
        result = []
        seen = set()
        for value in values:
            if value:
                normalized = os.path.normcase(os.path.abspath(value))
                if normalized not in seen:
                    seen.add(normalized)
                    result.append(value)
        return result

    def scan(self, progress_callback=None):
        results = []
        seen_paths = set()
        candidates = []
        for path in self.scan_paths:
            if path.exists() and path.is_dir():
                candidates.extend(self._collect_candidates(path))
        unique_candidates = list(dict.fromkeys(candidates))
        total = len(unique_candidates)
        if progress_callback:
            progress_callback(0, total, f"已发现 {total} 个候选文件")
        for index, path in enumerate(unique_candidates, 1):
            for result in self._scan_candidate(path):
                key = (result.get("path"), result.get("detector"))
                if key not in seen_paths:
                    seen_paths.add(key)
                    results.append(result)
            if progress_callback:
                progress_callback(index, total, f"正在校验 {path.name}")
        return results

    def scan_directory(self, directory):
        results = []
        for path in self._collect_candidates(directory):
            results.extend(self._scan_candidate(path))
        return results

    def _collect_candidates(self, directory):
        candidates = []
        for root, dirs, files in os.walk(directory, onerror=self._on_walk_error):
            # Avoid recursively scanning our own quarantine and common caches.
            dirs[:] = [
                name for name in dirs
                if name.lower() not in {"quarantine", "$recycle.bin", "node_modules", ".git"}
            ]
            for name in files:
                path = Path(root) / name
                if (self.is_malicious_filename(name)
                        or path.suffix.lower() in self.EXECUTABLE_EXTENSIONS):
                    candidates.append(path)
        return candidates

    def _scan_candidate(self, path):
        results = []
        name = path.name
        try:
            lure_match = self.is_malicious_filename(name)
            hashes = self.calculate_file_hashes(path)
            matched = self.match_malicious_hash(hashes)
            if matched:
                algorithm, value = matched
                results.append({
                    "type": "file",
                    "severity": "critical",
                    "confidence": "confirmed",
                    "path": str(path),
                    "sha256": hashes.get("sha256"),
                    "detail": f"已知恶意{algorithm.upper()}哈希命中: {value}",
                    "detector": "known_hash",
                    "action": "recommend_quarantine",
                    "remediable": True,
                })
            elif lure_match:
                results.append({
                    "type": "file",
                    "severity": "medium",
                    "confidence": "low",
                    "path": str(path),
                    "sha256": hashes.get("sha256"),
                    "detail": f"文件名符合银狐常见诱饵主题: {name}",
                    "detector": "lure_filename",
                    "action": "recommend_investigate",
                    "remediable": False,
                })
            elif self.is_suspicious_location(path):
                results.append({
                    "type": "file",
                    "severity": "low",
                    "confidence": "low",
                    "path": str(path),
                    "sha256": hashes.get("sha256"),
                    "detail": "用户临时目录中的可执行内容（仅线索）",
                    "detector": "executable_in_temp",
                    "action": "recommend_investigate",
                    "remediable": False,
                })
        except (OSError, PermissionError) as exc:
            if self.verbose:
                print(f"跳过无法读取的文件 {path}: {exc}")
        return results

    def _on_walk_error(self, error):
        if self.verbose:
            print(f"跳过无法访问的目录: {error}")

    def is_malicious_filename(self, filename):
        lowered = filename.casefold()
        return any(pattern.casefold() in lowered for pattern in self.LURE_PATTERNS)

    def calculate_file_hashes(self, file_path):
        try:
            path = Path(file_path)
            if path.stat().st_size > self.MAX_HASH_SIZE:
                return {}
            digests = {
                "md5": hashlib.md5(),  # nosec: compatibility with published IOC
                "sha1": hashlib.sha1(),  # nosec: compatibility with published IOC
                "sha256": hashlib.sha256(),
            }
            with path.open("rb") as handle:
                for block in iter(lambda: handle.read(1024 * 1024), b""):
                    for digest in digests.values():
                        digest.update(block)
            return {name: digest.hexdigest() for name, digest in digests.items()}
        except (OSError, PermissionError):
            return {}

    def calculate_file_hash(self, file_path):
        """Backward-compatible SHA-256 helper."""
        return self.calculate_file_hashes(file_path).get("sha256")

    def match_malicious_hash(self, hashes):
        known = set(self.malicious_hashes.get_hashes())
        for algorithm, value in hashes.items():
            if value.lower() in known:
                return algorithm, value
        return None

    def is_malicious_hash(self, file_hash):
        return self.malicious_hashes.is_malicious(file_hash)

    @staticmethod
    def is_suspicious_location(file_path):
        path = os.path.normcase(os.path.abspath(str(file_path)))
        candidates = [os.environ.get("TEMP"), os.environ.get("TMP")]
        return any(
            path == os.path.normcase(os.path.abspath(item))
            or path.startswith(os.path.normcase(os.path.abspath(item)) + os.sep)
            for item in candidates if item
        )
