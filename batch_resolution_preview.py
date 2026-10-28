"""Plan multiple video output sizes from a CSV, without opening media files."""

import argparse
import csv
import json
from pathlib import Path
import sys

from resolution_preview import plan_dimensions

MAX_DIMENSION = 100000


def parse_dimension(value):
    """Accept only bounded positive decimal pixel dimensions."""
    if value is None or not value.strip().isascii() or not value.strip().isdigit():
        raise ValueError("dimensions must be decimal integers")
    number = int(value.strip())
    if not 2 <= number <= MAX_DIMENSION:
        raise ValueError("dimensions must be between 2 and 100000")
    return number


def plan_batch(path, max_width, max_height, *, allow_upscale=True):
    """Return per-row previews and errors, never filenames or media content."""
    max_width = parse_dimension(str(max_width))
    max_height = parse_dimension(str(max_height))
    previews = []
    errors = []
    rows = 0
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        fields = reader.fieldnames or []
        if len(fields) != 2 or set(fields) != {"width", "height"}:
            raise ValueError("CSV must contain only width,height columns")
        for row in reader:
            rows += 1
            line = reader.line_num
            if None in row or any(value is None for value in row.values()):
                errors.append({"line": line, "reason": "column count mismatch"})
                continue
            try:
                width = parse_dimension(row["width"])
                height = parse_dimension(row["height"])
                output_width, output_height = plan_dimensions(
                    width, height, max_width, max_height,
                    allow_upscale=allow_upscale,
                )
            except ValueError as exc:
                errors.append({"line": line, "reason": str(exc)})
                continue
            previews.append({
                "line": line,
                "input": [width, height],
                "output": [output_width, output_height],
                "ffmpeg_scale_filter": f"scale={output_width}:{output_height}:flags=lanczos",
            })
    return {
        "ok": rows > 0 and not errors,
        "rows": rows,
        "previews": previews,
        "invalid_rows": errors,
        "upscale_allowed": allow_upscale,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="CSV with width,height columns")
    parser.add_argument("max_width", type=int, help="target bounding-box width")
    parser.add_argument("max_height", type=int, help="target bounding-box height")
    parser.add_argument("--no-upscale", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = plan_batch(
            args.csv_file, args.max_width, args.max_height,
            allow_upscale=not args.no_upscale,
        )
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for preview in report["previews"]:
            print(f"Line {preview['line']}: {preview['input']} -> {preview['output']}")
        print(f"Rows: {report['rows']} | Invalid: {len(report['invalid_rows'])}")
        print("Preview only: no video was read or converted.")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
