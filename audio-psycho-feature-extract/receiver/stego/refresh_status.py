#!/usr/bin/env python3
from pathlib import Path

WORKDIR = Path.home() / "stego"
RESULT = Path.home() / ".local" / "result" / "psycho_check.txt"

def main():
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    tokens = []
    cover = WORKDIR / "cover.wav"
    stego = WORKDIR / "stego.wav"
    recovered = WORKDIR / "recovered.txt"
    expected = WORKDIR / ".expected_message.txt"
    viewed = WORKDIR / ".recovered_viewed"
    if cover.is_file() and cover.stat().st_size > 0 and stego.is_file() and stego.stat().st_size > 0:
        tokens.append("PASS_AUDIO_RECEIVED")
    if recovered.is_file() and recovered.stat().st_size > 0:
        tokens.append("PASS_RECOVERED_CREATED")
    if (
        recovered.is_file()
        and expected.is_file()
        and viewed.is_file()
        and viewed.stat().st_mtime >= recovered.stat().st_mtime
        and recovered.read_bytes().rstrip(b"\r\n") == expected.read_bytes().rstrip(b"\r\n")
    ):
        tokens.append("PASS_MESSAGE_RECOVERED")
    RESULT.write_text("\n".join(tokens) + ("\n" if tokens else ""), encoding="utf-8")

if __name__ == "__main__":
    main()
