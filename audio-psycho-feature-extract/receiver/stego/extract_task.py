#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


COVER_FILE = "TODO_COVER_FILENAME"
STEGO_FILE = "TODO_STEGO_FILENAME"
OUTPUT_FILE = "recovered.txt"


def validate_placeholder(value, name):
    if not value or value.startswith("TODO_"):
        raise ValueError(f"Please edit {name} in extract_task.py before running.")


def main():
    validate_placeholder(COVER_FILE, "COVER_FILE")
    validate_placeholder(STEGO_FILE, "STEGO_FILE")
    workdir = Path(__file__).resolve().parent
    cover = workdir / COVER_FILE
    stego = workdir / STEGO_FILE
    if not cover.is_file():
        raise FileNotFoundError(f"Input file not found: {cover.name}")
    if not stego.is_file():
        raise FileNotFoundError(f"Input file not found: {stego.name}")
    viewed = workdir / ".recovered_viewed"
    if viewed.exists():
        viewed.unlink()
    cmd = [
        sys.executable,
        str(workdir / "psycho_feature_stego.py"),
        "extract",
        "--cover",
        COVER_FILE,
        "--stego",
        STEGO_FILE,
        "--out",
        OUTPUT_FILE,
    ]
    subprocess.run(cmd, cwd=str(workdir), check=True)
    print(f"Created {OUTPUT_FILE}. Run: cat {OUTPUT_FILE}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
