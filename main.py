"""Entry point for the news-image-20261121 competition.

The front page image (entry.png) is drawn by draw.py with PIL and ships in
this repository. This program only copies it to the output directory as
entry.png, so it needs nothing but the Python standard library, uses no
network, and writes byte-identical output on every run.
"""

import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1048576
MAX_DIM = 1024


def check_png(path):
    """Fail loudly if the shipped image would fail the competition gate:
    must be a whole PNG, at most 1 MiB and at most 1024x1024."""
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError("entry.png is %dx%d, over the 1024x1024 limit"
                         % (width, height))
    if os.path.getsize(path) > MAX_BYTES:
        raise ValueError("entry.png is over the 1 MiB limit")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        raise FileNotFoundError("entry.png is missing next to main.py")

    check_png(src)
    shutil.copyfile(src, dst)
    check_png(dst)


if __name__ == "__main__":
    main()
