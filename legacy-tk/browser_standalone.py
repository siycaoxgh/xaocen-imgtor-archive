#!/usr/bin/env python3
"""Standalone image browser entry point."""
import os, sys, json, tkinter as tk

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

config_path = os.path.join(BASE, 'config.json')
save_dir = ''
if os.path.exists(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    save_dir = cfg.get('save_directory', '')
if not save_dir:
    save_dir = os.path.join(os.path.expanduser('~'), 'Pictures', 'drawru-imgter')

from browser import ImageBrowser

root = tk.Tk()
root.withdraw()
browser = ImageBrowser(save_dir)
browser.run()

def close_root(event=None):
    # ImageBrowser uses a Toplevel.  Destroy the hidden owner when that
    # window closes so this compatibility process cannot keep mainloop alive.
    if event is None or event.widget is browser.root:
        try:
            root.destroy()
        except tk.TclError:
            pass

if browser.root is not None:
    browser.root.bind('<Destroy>', close_root, add='+')
try:
    root.mainloop()
finally:
    try:
        root.destroy()
    except tk.TclError:
        pass
