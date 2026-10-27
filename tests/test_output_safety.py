import os
import tempfile
import unittest
from pathlib import Path

from output_safety import validate_output_path


class OutputSafetyTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.source = Path(self.folder.name) / "input.mp4"
        self.source.write_bytes(b"sample")

    def test_new_output_is_accepted(self):
        target = Path(self.folder.name) / "upscaled.mp4"
        self.assertEqual(validate_output_path(self.source, target), str(target))

    def test_same_path_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "aynı"):
            validate_output_path(self.source, self.source)

    def test_existing_other_file_is_rejected(self):
        target = Path(self.folder.name) / "already.mp4"
        target.write_bytes(b"keep")
        with self.assertRaisesRegex(ValueError, "zaten var"):
            validate_output_path(self.source, target)
        self.assertEqual(target.read_bytes(), b"keep")

    def test_hardlink_alias_is_rejected(self):
        alias = Path(self.folder.name) / "alias.mp4"
        os.link(self.source, alias)
        with self.assertRaises(ValueError):
            validate_output_path(self.source, alias)

    def test_symlink_alias_is_rejected(self):
        alias = Path(self.folder.name) / "alias.mp4"
        alias.symlink_to(self.source)
        with self.assertRaisesRegex(ValueError, "aynı"):
            validate_output_path(self.source, alias)

    def test_missing_input_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "bulunamadı"):
            validate_output_path(Path(self.folder.name) / "missing.mp4", "new.mp4")

    def test_missing_parent_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "klasörü"):
            validate_output_path(self.source, Path(self.folder.name) / "absent" / "new.mp4")

    def test_empty_output_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "çıkış"):
            validate_output_path(self.source, "")


if __name__ == "__main__":
    unittest.main()
