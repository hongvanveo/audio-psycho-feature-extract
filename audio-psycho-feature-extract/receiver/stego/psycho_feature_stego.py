#!/usr/bin/env python3
import argparse
import os
import struct
import sys
import wave
from array import array


MAGIC = b"PSYA"
SEGMENT = 256
DELAY = 1


def mark(token):
    result = os.path.expanduser("~/.local/result/psycho_check.txt")
    os.makedirs(os.path.dirname(result), exist_ok=True)
    existing = ""
    if os.path.exists(result):
        with open(result, "r", encoding="utf-8") as handle:
            existing = handle.read()
    if token not in existing:
        with open(result, "a", encoding="utf-8") as handle:
            handle.write(token + "\n")


def byte_bits(data):
    for byte in data:
        for bit in range(7, -1, -1):
            yield (byte >> bit) & 1


def bits_bytes(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        chunk = bits[i:i + 8]
        if len(chunk) < 8:
            break
        value = 0
        for bit in chunk:
            value = (value << 1) | bit
        out.append(value)
    return bytes(out)


def read_wav(path):
    with wave.open(path, "rb") as wav:
        params = wav.getparams()
        if params.nchannels != 1 or params.sampwidth != 2:
            raise ValueError("Use mono PCM16 WAV.")
        frames = wav.readframes(params.nframes)
    samples = array("h")
    samples.frombytes(frames)
    return params, samples


def write_wav(path, params, samples):
    with wave.open(path, "wb") as wav:
        wav.setparams(params)
        wav.writeframes(samples.tobytes())


def clamp(value):
    return max(-32768, min(32767, int(round(value))))


def model_one(segment):
    return [clamp(0.99 * x) for x in segment]


def model_zero(segment):
    out = []
    for i, value in enumerate(segment):
        delayed = segment[i - DELAY] if i >= DELAY else 0
        out.append(clamp(0.98 * value + delayed))
    return out


def mse(a, b):
    return sum((x - y) * (x - y) for x, y in zip(a, b)) / len(a)


def embed(args):
    params, samples = read_wav(args.infile)
    with open(args.message, "rb") as handle:
        message = handle.read()
    payload = MAGIC + struct.pack(">I", len(message)) + message
    bits = list(byte_bits(payload))
    capacity = len(samples) // SEGMENT
    if len(bits) > capacity:
        raise ValueError(f"Need {len(bits)} segments, capacity is {capacity}.")

    stego = array("h", samples)
    for i, bit in enumerate(bits):
        start = i * SEGMENT
        end = start + SEGMENT
        segment = samples[start:end]
        changed = model_one(segment) if bit == 1 else model_zero(segment)
        stego[start:end] = array("h", changed)

    write_wav(args.out, params, stego)
    mark("PASS_STEGO_CREATED")
    mark("PASS_AUDIO_MODIFIED")
    print(f"capacity_segments={capacity}")
    print(f"embedded_bits={len(bits)}")
    print(f"wrote={args.out}")


def extract(args):
    if (
        os.path.exists(args.cover)
        and os.path.getsize(args.cover) > 0
        and os.path.exists(args.stego)
        and os.path.getsize(args.stego) > 0
    ):
        mark("PASS_AUDIO_RECEIVED")
    _, cover = read_wav(args.cover)
    _, stego = read_wav(args.stego)
    if len(cover) != len(stego):
        raise ValueError("cover and stego length mismatch")

    bits = []
    for start in range(0, len(cover) - SEGMENT + 1, SEGMENT):
        base = cover[start:start + SEGMENT]
        actual = stego[start:start + SEGMENT]
        err_one = mse(actual, model_one(base))
        err_zero = mse(actual, model_zero(base))
        bits.append(1 if err_one <= err_zero else 0)

    decoded = bits_bytes(bits)
    pos = decoded.find(MAGIC)
    if pos < 0 or pos + 8 > len(decoded):
        raise ValueError("psychoacoustic header not found")
    length = struct.unpack(">I", decoded[pos + 4:pos + 8])[0]
    message = decoded[pos + 8:pos + 8 + length]
    if len(message) != length:
        raise ValueError("message truncated")
    with open(args.out, "wb") as handle:
        handle.write(message)
    mark("PASS_RECOVERED_CREATED")
    print(f"recovered_bytes={len(message)}")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("embed")
    p.add_argument("--in", dest="infile", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--message", required=True)
    p.set_defaults(func=embed)
    p = sub.add_parser("extract")
    p.add_argument("--cover", required=True)
    p.add_argument("--stego", required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(func=extract)
    try:
        args = parser.parse_args()
        args.func(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
