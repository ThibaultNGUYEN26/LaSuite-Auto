import tempfile
import unittest
from pathlib import Path

from agent.base import DelegationContext
from agent.errors import LocalFilesError
from agent.specialists.local_files import LocalFilesReadTextAgent
from services.local_files import read_local_text


class LocalTextReaderTests(unittest.TestCase):
    def test_reads_utf8_csv_with_bom_and_accents(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Titi.csv").write_text(
                "année,surface pâturale\n2025,48.7\n",
                encoding="utf-8-sig",
            )

            result = read_local_text(
                root,
                "Titi.csv",
                max_bytes=1000,
                max_characters=1000,
            )

            self.assertEqual(result["encoding"], "utf-8-sig")
            self.assertEqual(
                result["content"].splitlines(),
                ["année,surface pâturale", "2025,48.7"],
            )
            self.assertNotIn("\ufeff", result["content"])
            self.assertFalse(result["truncated"])

    def test_reads_windows_1252_text(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "legacy.csv").write_bytes("région,valeur\nété,3\n".encode("cp1252"))

            result = read_local_text(
                root,
                "legacy.csv",
                max_bytes=1000,
                max_characters=1000,
            )

            self.assertEqual(result["encoding"], "cp1252")
            self.assertIn("région", result["content"])

    def test_bounds_returned_text(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "large.txt").write_text("abcdefghij", encoding="utf-8")

            result = read_local_text(
                root,
                "large.txt",
                max_bytes=1000,
                max_characters=5,
            )

            self.assertEqual(result["content"], "abcde")
            self.assertTrue(result["truncated"])
            self.assertEqual(result["characters"], 10)

    def test_rejects_an_unsupported_binary_extension(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "archive.zip").write_bytes(b"PK-test")

            with self.assertRaisesRegex(LocalFilesError, "Unsupported text file"):
                read_local_text(
                    root,
                    "archive.zip",
                    max_bytes=1000,
                    max_characters=1000,
                )

    def test_agent_consumes_a_local_file_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data.json").write_text('{"title": "Pasture"}', encoding="utf-8")
            agent = LocalFilesReadTextAgent(root)

            result = agent.execute(
                {
                    "artifact": {
                        "kind": "file",
                        "location": "local",
                        "reference": "data.json",
                        "media_type": "application/json",
                        "name": "data.json",
                        "metadata": {},
                    }
                },
                DelegationContext(conversation=()),
            )

            self.assertIn("Pasture", result["content"])
            self.assertEqual(result["artifact"]["reference"], "data.json")


if __name__ == "__main__":
    unittest.main()
