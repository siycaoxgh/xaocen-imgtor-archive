#!/usr/bin/env python3
"""Compatibility entry point.

The product has one user-facing UI now: webapp.py + ui/index.html.
This file remains only so older shortcuts that still call gui.py continue to
open the same application instead of starting a second Tkinter launcher.
"""

from webapp import main


if __name__ == '__main__':
    main()
