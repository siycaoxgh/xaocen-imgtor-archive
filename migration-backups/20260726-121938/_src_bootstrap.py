"""Make the src-layout package importable from source and worker entrypoints."""

from pathlib import Path
import sys


def ensure_src_path():
    src = str(Path(__file__).resolve().parent / 'src')
    if src not in sys.path:
        sys.path.insert(0, src)


ensure_src_path()
