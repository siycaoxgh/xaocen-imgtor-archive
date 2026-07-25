#!/usr/bin/env python3
"""Standalone image crop entry point."""
import os, sys, tkinter as tk

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from cropper import ImageCropper

root = tk.Tk()
root.withdraw()
c = ImageCropper()
c.run()

def close_root(event=None):
    if event is None or event.widget is c.root:
        try:
            root.destroy()
        except tk.TclError:
            pass

if c.root is not None:
    c.root.bind('<Destroy>', close_root, add='+')
try:
    root.mainloop()
finally:
    try:
        root.destroy()
    except tk.TclError:
        pass
