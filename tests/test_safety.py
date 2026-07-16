import tempfile
import unittest
from pathlib import Path

from cleaner.file_cleaner import FileCleaner
from ioc.domains import MaliciousDomains
from quarantine import QuarantineManager
from scanner.file_scanner import FileScanner


class QuarantineTests(unittest.TestCase):
    def test_quarantine_and_restore_round_trip(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original = root / "sample.exe"
            original.write_bytes(b"harmless test fixture")
            manager = QuarantineManager(root / "quarantine")

            entry = manager.quarantine(str(original), "unit test")
            self.assertFalse(original.exists())
            self.assertTrue(Path(entry["quarantine_path"]).exists())
            self.assertEqual(manager.list()[0]["id"], entry["id"])

            restored = manager.restore(entry["id"])
            self.assertEqual(restored["status"], "restored")
            self.assertEqual(original.read_bytes(), b"harmless test fixture")
            self.assertEqual(manager.list(), [])

    def test_cleaner_refuses_heuristic_detection(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            candidate = root / "candidate.exe"
            candidate.write_bytes(b"not malware")
            cleaner = FileCleaner(quarantine_manager=QuarantineManager(root / "q"))
            result = cleaner.clean_file({
                "path": str(candidate), "confidence": "low", "remediable": False,
            })
            self.assertTrue(result["skipped"])
            self.assertTrue(candidate.exists())


class DetectionTests(unittest.TestCase):
    def test_lure_name_is_report_only(self):
        with tempfile.TemporaryDirectory() as temp:
            candidate = Path(temp) / "内部调查结果.exe"
            candidate.write_bytes(b"benign fixture")
            result = FileScanner(scan_paths=[temp]).scan()
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["detector"], "lure_filename")
            self.assertFalse(result[0]["remediable"])

    def test_file_progress_is_based_on_real_candidate_count(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "a.exe").write_bytes(b"fixture a")
            (root / "ignored.txt").write_bytes(b"fixture b")
            updates = []
            FileScanner(scan_paths=[temp]).scan(
                lambda current, total, message: updates.append((current, total)))
            self.assertEqual(updates[0], (0, 1))
            self.assertEqual(updates[-1], (1, 1))

    def test_domain_matching_respects_label_boundary(self):
        domains = MaliciousDomains()
        self.assertTrue(domains.is_malicious("sub.vauwjw.net"))
        self.assertFalse(domains.is_malicious("notvauwjw.net"))


if __name__ == "__main__":
    unittest.main()
