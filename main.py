"""Entry program for news-image-20261121.

Copies the pre-rendered front page (frontpage.png, drawn by render.py)
to the output directory as entry.png. Deterministic: the same input
bytes always produce the same output bytes. The output is checked to
be a real PNG before the program reports success.
"""

import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontpage.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    with open(dest, "rb") as fh:
        head = fh.read(8)
    if head != PNG_MAGIC:
        print("error: entry.png is not a PNG", file=sys.stderr)
        raise SystemExit(1)
    print("wrote %s (%d bytes)" % (dest, os.path.getsize(dest)))


if __name__ == "__main__":
    main()
