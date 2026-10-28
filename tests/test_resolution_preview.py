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
        self.assertEqual(result["input_pixels"], 1920 * 1080)
        self.assertEqual(result["output_pixels"], 1280 * 720)
        self.assertEqual(result["pixel_ratio"], 0.444)


    def test_cli_upscale_pixel_ratio(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["640", "480", "1280", "960", "--json"]), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["pixel_ratio"], 4.0)
        self.assertEqual(result["output_pixels"], 1280 * 960)

    def test_cli_no_upscale_pixel_ratio(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["640", "480", "1280", "960", "--no-upscale", "--json"]), 0)
        self.assertEqual(json.loads(output.getvalue())["pixel_ratio"], 1.0)

    def test_text_output_mentions_pixel_load(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["1920", "1080", "1280", "720"]), 0)
        self.assertIn("Pixel load: 921,600 output pixels", output.getvalue())


if __name__ == "__main__":
    unittest.main()
