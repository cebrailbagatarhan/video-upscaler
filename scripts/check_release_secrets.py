"""Fail when release signing material or generated Android binaries are tracked."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {".keystore", ".jks", ".p12", ".apk", ".aab", ".zip"}
TEXT_SUFFIXES = {".spec", ".sh", ".bat", ".yml", ".yaml", ".py"}
IGNORED_PARTS = {".git", ".buildozer", "bin", "artifacts", ".venv", "venv"}

SPEC_SECRET = re.compile(
    r"^\s*android\.release_(?:keystore|keystore_passwd|key_alias|key_passwd)\s*=\s*\S+",
    re.MULTILINE,
)
SHELL_PASSWORD_LITERAL = re.compile(
    r"^\s*(?:export\s+)?P4A_RELEASE_(?:KEYSTORE_PASSWD|KEYALIAS_PASSWD)\s*=\s*(?![\"']?\$)[^\s#]+",
    re.MULTILINE,
)


def tracked_files() -> list[Path]:
    try:
        output = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files", "-z"], stderr=subprocess.DEVNULL
        )
        return [ROOT / item.decode("utf-8") for item in output.split(b"\0") if item]
    except (OSError, subprocess.CalledProcessError):
        return [
            path
            for path in ROOT.rglob("*")
            if path.is_file() and not IGNORED_PARTS.intersection(path.relative_to(ROOT).parts)
        ]


def main() -> int:
    failures: list[str] = []
    for path in tracked_files():
        relative = path.relative_to(ROOT)
        if path.suffix.casefold() in FORBIDDEN_SUFFIXES:
            failures.append(f"tracked release/build artifact: {relative}")
            continue
        if path.suffix.casefold() not in TEXT_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if SPEC_SECRET.search(content):
            failures.append(f"release signing value in config: {relative}")
        if SHELL_PASSWORD_LITERAL.search(content):
            failures.append(f"release signing password literal in script: {relative}")

    if failures:
        print("\n".join(failures))
        return 1
    print("Release secret regression check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
