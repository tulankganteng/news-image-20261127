#!/usr/bin/env python3
"""news-image-20261127 entrypoint (Python 3.13, standard library only).

Copies the pre-rendered front page (entry.png, in this repository) to the
output directory as entry.png. No network, no third-party packages.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1048576  # the gate allows at most 1 MiB


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    if os.path.getsize(src) > MAX_BYTES:
        print(f"entry.png is {os.path.getsize(src)} bytes, over the 1 MiB gate",
              file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    if sha256_file(src) != sha256_file(dst):
        print("copy verification failed: hashes differ", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
