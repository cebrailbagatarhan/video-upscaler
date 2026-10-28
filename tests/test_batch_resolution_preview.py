import contextlib
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest

from batch_resolution_preview import main, parse_dimension, plan_batch


class BatchResolutionPreviewTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name) / "dimensions.csv"

    def write(self, rows, fields=("width", "height")):
        with self.path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(fields)
            writer.writerows(rows)

    def test_multiple_orientations(self):
        self.write([["1920", "1080"], ["1080", "1920"]])
        report = plan_batch(self.path, 1280, 720)
        self.assertTrue(report["ok"])
        self.assertEqual([r["output"] for r in report["previews"]], [[1280, 720], [404, 720]])

    def test_no_upscale(self):
        self.write([["640", "480"]])
        report = plan_batch(self.path, 1920, 1080, allow_upscale=False)
        self.assertEqual(report["previews"][0]["output"], [640, 480])
        self.assertFalse(report["upscale_allowed"])

    def test_bad_rows_do_not_prevent_other_previews(self):
        self.write([["x", "1080"], ["800", "600"], ["640"]])
        report = plan_batch(self.path, 400, 300)
        self.assertFalse(report["ok"])
        self.assertEqual(report["rows"], 3)
        self.assertEqual(len(report["previews"]), 1)
        self.assertEqual([r["line"] for r in report["invalid_rows"]], [2, 4])

    def test_rejects_bad_headers(self):
        self.write([], fields=("width", "width"))
        with self.assertRaises(ValueError):
            plan_batch(self.path, 100, 100)

    def test_empty_csv_is_not_ok(self):
        self.write([])
        self.assertFalse(plan_batch(self.path, 100, 100)["ok"])

    def test_dimension_limits_and_non_ascii(self):
        for value in ("1", "-2", "100001", "2.5", "²", ""):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_dimension(value)
        self.assertEqual(parse_dimension(" 200 "), 200)

    def test_cli_json_and_status(self):
        self.write([["1920", "1080"]])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main([str(self.path), "1280", "720", "--json"]), 0)
        self.assertEqual(json.loads(output.getvalue())["previews"][0]["output"], [1280, 720])
        self.assertEqual(main([str(self.path) + ".missing", "1280", "720"]), 2)

    def test_rejects_invalid_target(self):
        self.write([["1920", "1080"]])
        with self.assertRaises(ValueError):
            plan_batch(self.path, 0, 720)


if __name__ == "__main__":
    unittest.main()
