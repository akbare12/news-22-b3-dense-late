#!/usr/bin/env python3
"""Copy entry.png to the output directory (standard library only)."""
import hashlib
import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    with open(SRC, "rb") as f:
        src_data = f.read()
    src_sha = hashlib.sha256(src_data).hexdigest()
    with open(dst, "rb") as f:
        dst_data = f.read()
    dst_sha = hashlib.sha256(dst_data).hexdigest()
    if src_sha != dst_sha:
        print("sha256 mismatch", file=sys.stderr)
        return 1
    if len(src_data) != len(dst_data):
        print("size mismatch", file=sys.stderr)
        return 1
    print("wrote", dst, len(dst_data), "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
