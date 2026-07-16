"""Reversible local quarantine used by the Windows cleaner.

Quarantined files are moved out of their original location and renamed with a
non-executable suffix.  A JSON manifest keeps enough information to restore
them.  The implementation deliberately never uploads samples.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path


def default_data_dir() -> Path:
    base = os.environ.get("PROGRAMDATA") or os.environ.get("LOCALAPPDATA")
    if not base:
        base = str(Path.home() / ".silverfox-killer")
    return Path(base) / "SilverFoxKiller"


class QuarantineManager:
    """Move, list and restore quarantined files with an atomic manifest."""

    def __init__(self, root: str | os.PathLike[str] | None = None):
        self.root = Path(root) if root else default_data_dir() / "Quarantine"
        self.files_dir = self.root / "files"
        self.manifest_path = self.root / "manifest.json"
        self._lock = threading.Lock()
        self.files_dir.mkdir(parents=True, exist_ok=True)
        if not self.manifest_path.exists():
            self._write_manifest([])

    @staticmethod
    def sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _read_manifest(self) -> list[dict]:
        try:
            data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    def _write_manifest(self, entries: list[dict]) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        temp = self.manifest_path.with_suffix(".tmp")
        temp.write_text(
            json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        os.replace(temp, self.manifest_path)

    def quarantine(self, file_path: str, reason: str = "") -> dict:
        source = Path(file_path).resolve(strict=True)
        if not source.is_file():
            raise ValueError(f"不是普通文件: {source}")

        item_id = uuid.uuid4().hex
        file_hash = self.sha256(source)
        destination = self.files_dir / f"{item_id}.quarantine"
        shutil.move(str(source), str(destination))

        entry = {
            "id": item_id,
            "original_path": str(source),
            "quarantine_path": str(destination),
            "original_name": source.name,
            "sha256": file_hash,
            "size": destination.stat().st_size,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "quarantined",
        }
        try:
            with self._lock:
                entries = self._read_manifest()
                entries.append(entry)
                self._write_manifest(entries)
        except Exception:
            shutil.move(str(destination), str(source))
            raise
        return entry

    def list(self, include_restored: bool = False) -> list[dict]:
        entries = self._read_manifest()
        if include_restored:
            return entries
        return [entry for entry in entries if entry.get("status") == "quarantined"]

    def restore(self, item_id: str, overwrite: bool = False) -> dict:
        with self._lock:
            entries = self._read_manifest()
            entry = next((item for item in entries if item.get("id") == item_id), None)
            if not entry:
                raise KeyError(f"未找到隔离项: {item_id}")
            if entry.get("status") != "quarantined":
                raise ValueError("该隔离项已恢复")

            source = Path(entry["quarantine_path"])
            destination = Path(entry["original_path"])
            if not source.is_file():
                raise FileNotFoundError(f"隔离文件不存在: {source}")
            if destination.exists() and not overwrite:
                raise FileExistsError(f"原位置已有文件: {destination}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                destination.unlink()
            shutil.move(str(source), str(destination))
            entry["status"] = "restored"
            entry["restored_at"] = datetime.now(timezone.utc).isoformat()
            self._write_manifest(entries)
            return entry
