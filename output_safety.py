"""Preflight checks that keep FFmpeg from overwriting a source or existing file."""

from pathlib import Path


def validate_output_path(input_path, output_path):
    """Raise ValueError unless input exists and output is a new file in a real folder.

    This is a usability guard, not a replacement for FFmpeg's ``-n`` race guard.
    """
    if not input_path or not str(input_path).strip():
        raise ValueError("Lütfen önce bir giriş dosyası seçin.")
    if not output_path or not str(output_path).strip():
        raise ValueError("Lütfen bir çıkış dosyası adı girin.")

    source = Path(input_path).expanduser()
    target = Path(output_path).expanduser()
    if not source.is_file():
        raise ValueError("Giriş dosyası bulunamadı.")
    if not target.parent.is_dir():
        raise ValueError("Çıkış klasörü bulunamadı.")
    if source.resolve() == target.resolve():
        raise ValueError("Çıkış dosyası giriş dosyasıyla aynı olamaz.")
    if target.exists() or target.is_symlink():
        raise ValueError("Çıkış dosyası zaten var. Lütfen farklı bir ad seçin.")
    return str(target)
