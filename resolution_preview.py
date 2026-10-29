"""Preview aspect-ratio-preserving output dimensions without processing media.

This is a standalone planning helper; it does not change the Kivy application's
current scaling behavior or claim AI super-resolution.
"""

import argparse
import json
import math


def plan_dimensions(width, height, max_width, max_height, *, allow_upscale=True,
                    max_upscale_factor=None):
    """Return even dimensions that fit inside the target box.

    Even dimensions are suitable for common 4:2:0 video encoders. Rounding can
    change the exact aspect ratio by up to a couple of pixels.
    """
    dimensions = (width, height, max_width, max_height)
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 2 for value in dimensions):
        raise ValueError("all dimensions must be integers >= 2")
    if max_upscale_factor is not None:
        if (isinstance(max_upscale_factor, bool)
                or not isinstance(max_upscale_factor, (int, float))
                or not math.isfinite(max_upscale_factor)
                or max_upscale_factor < 1):
            raise ValueError("max_upscale_factor must be finite and >= 1")
    factor = min(max_width / width, max_height / height)
    if max_upscale_factor is not None:
        factor = min(factor, max_upscale_factor)
    if not allow_upscale:
        factor = min(factor, 1.0)
    scaled_width = math.floor(width * factor / 2) * 2
    scaled_height = math.floor(height * factor / 2) * 2
    if min(scaled_width, scaled_height) < 2:
        raise ValueError("resulting dimensions would be smaller than 2 pixels")
    return scaled_width, scaled_height


def main(argv=None):
    parser = argparse.ArgumentParser(description="Preview even-sized, aspect-preserving video output dimensions")
    parser.add_argument("width", type=int, help="input width in pixels")
    parser.add_argument("height", type=int, help="input height in pixels")
    parser.add_argument("max_width", type=int, help="target bounding-box width")
    parser.add_argument("max_height", type=int, help="target bounding-box height")
    parser.add_argument("--no-upscale", action="store_true", help="never enlarge the input")
    parser.add_argument("--max-upscale-factor", type=float,
                        help="limit enlargement to this multiple of source size (>= 1)")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args(argv)
    try:
        out_width, out_height = plan_dimensions(
            args.width, args.height, args.max_width, args.max_height,
            allow_upscale=not args.no_upscale,
            max_upscale_factor=args.max_upscale_factor,
        )
    except ValueError as exc:
        parser.error(str(exc))
    result = {
        "input": [args.width, args.height],
        "target_box": [args.max_width, args.max_height],
        "output": [out_width, out_height],
        "upscale_allowed": not args.no_upscale,
        "ffmpeg_scale_filter": f"scale={out_width}:{out_height}:flags=lanczos",
    }
    if args.max_upscale_factor is not None:
        result["max_upscale_factor"] = args.max_upscale_factor
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"Preview: {args.width}x{args.height} -> {out_width}x{out_height}")
        print(f"Suggested FFmpeg filter: {result['ffmpeg_scale_filter']}")
        print("Preview only: the Android/Kivy application is unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
