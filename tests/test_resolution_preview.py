import contextlib
import io
import json
import unittest

from resolution_preview import main, plan_dimensions


class ResolutionPreviewTests(unittest.TestCase):
    def test_landscape_fits_exactly(self):
        self.assertEqual(plan_dimensions(1920, 1080, 1280, 720), (1280, 720))

    def test_portrait_preserves_orientation_and_bounds(self):
        width, height = plan_dimensions(1080, 1920, 1920, 1080)
        self.assertEqual((width, height), (606, 1080))
        self.assertEqual(width % 2, 0)

    def test_no_upscale(self):
        self.assertEqual(plan_dimensions(640, 480, 1920, 1080, allow_upscale=False), (640, 480))

    def test_even_dimensions_with_odd_bounds(self):
        self.assertEqual(plan_dimensions(800, 600, 101, 101), (100, 74))

    def test_rejects_invalid_dimensions(self):
        for dims in ((0, 10, 20, 20), (1, 100, 200, 200), (100, 100, 1, 100)):
            with self.subTest(dims=dims), self.assertRaises(ValueError):
                plan_dimensions(*dims)

    def test_cli_json(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["1920", "1080", "1280", "720", "--json"]), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["output"], [1280, 720])
        self.assertEqual(result["ffmpeg_scale_filter"], "scale=1280:720:flags=lanczos")

    def test_max_upscale_factor_caps_enlargement(self):
        self.assertEqual(
            plan_dimensions(640, 360, 1920, 1080, max_upscale_factor=1.5),
            (960, 540),
        )
        self.assertEqual(
            plan_dimensions(640, 360, 1920, 1080, max_upscale_factor=1),
            (640, 360),
        )

    def test_no_upscale_overrides_factor_cap(self):
        self.assertEqual(
            plan_dimensions(640, 360, 1920, 1080, allow_upscale=False,
                            max_upscale_factor=3),
            (640, 360),
        )

    def test_rejects_invalid_max_upscale_factor(self):
        for factor in (0, 0.5, float("nan"), float("inf"), True):
            with self.subTest(factor=factor), self.assertRaises(ValueError):
                plan_dimensions(640, 360, 1920, 1080, max_upscale_factor=factor)

    def test_cli_reports_capped_dimensions(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["640", "360", "1920", "1080",
                                   "--max-upscale-factor", "1.5", "--json"]), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["output"], [960, 540])
        self.assertEqual(result["max_upscale_factor"], 1.5)


if __name__ == "__main__":
    unittest.main()
