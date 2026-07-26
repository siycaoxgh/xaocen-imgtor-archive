#!/usr/bin/env python3
"""
drawru-imgter Settings — i18n-aware GUI settings window
"""

import os, json, tkinter as tk
from tkinter import filedialog, messagebox
from config_manager import DEFAULT_CONFIG, load_config as load_central_config, save_config as save_central_config
from ratio_presets import ratio_options
from shortcuts import validate

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, 'config.json')

def load_config():
    return load_central_config()


def save_config(cfg):
    save_central_config(cfg)


class SettingsWindow:
    def __init__(self):
        self.config = load_config()
        from i18n import get as _t
        self.t = lambda k, **kw: _t(self.config, k, **kw)
        self.root = None

    def run(self):
        t = self.t
        self.root = tk.Tk()
        self.root.title(f'drawru-imgter — {t("settings.title")}')
        self.root.configure(bg='#f5f5f5')
        self.root.resizable(False, False)

        w, h = 540, 540
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f'{w}x{h}+{(sw-w)//2}+{(sh-h)//2}')
        self._build_ui()
        self.root.mainloop()

    def _build_ui(self):
        t = self.t
        frame = tk.Frame(self.root, bg='white', padx=20, pady=20)
        frame.pack(fill='both', expand=True)

        tk.Label(frame, text=f'drawru-imgter {t("settings.title")}',
                font=('Microsoft YaHei', 14, 'bold'), fg='#1a1a2e', bg='white'
                ).pack(anchor='w', pady=(0, 16))

        # Hotkey
        row = tk.Frame(frame, bg='white'); row.pack(fill='x', pady=3)
        tk.Label(row, text=t('settings.hotkey'), fg='#333', bg='white',
                font=('Microsoft YaHei', 10), width=14, anchor='w').pack(side='left')
        self.hk_var = tk.StringVar(value=self.config.get('hotkey', DEFAULT_CONFIG['hotkey']))
        tk.Entry(row, textvariable=self.hk_var, width=18, font=('Consolas', 10),
                bg='#f0f0f0', relief='flat').pack(side='left', padx=(0, 8))
        tk.Label(row, text=t('settings.hotkey_hint'), fg='#999', bg='white',
                font=('Microsoft YaHei', 8)).pack(side='left')
        tk.Label(row, text=t('settings.restart_note'), fg='#e67e22', bg='white',
                font=('Microsoft YaHei', 8)).pack(side='left', padx=(8, 0))

        # Save dir
        row = tk.Frame(frame, bg='white'); row.pack(fill='x', pady=3)
        tk.Label(row, text=t('settings.save_dir'), fg='#333', bg='white',
                font=('Microsoft YaHei', 10), width=14, anchor='w').pack(side='left')
        self.dir_var = tk.StringVar(value=self.config.get('save_directory', DEFAULT_CONFIG['save_directory']))
        tk.Entry(row, textvariable=self.dir_var, font=('Microsoft YaHei', 9),
                bg='#f0f0f0', relief='flat').pack(side='left', fill='x', expand=True)
        tk.Button(row, text=t('settings.browse'), command=self._browse_dir,
                 bg='#3498db', fg='white', font=('Microsoft YaHei', 8),
                 relief='flat', cursor='hand2', padx=8).pack(side='left', padx=(6, 0))

        # Default mode
        row = tk.Frame(frame, bg='white'); row.pack(fill='x', pady=3)
        tk.Label(row, text=t('settings.default_mode'), fg='#333', bg='white',
                font=('Microsoft YaHei', 10), width=14, anchor='w').pack(side='left')
        mf = tk.Frame(row, bg='white'); mf.pack(side='left')
        self.mode_var = tk.StringVar(value=self.config.get('default_mode', DEFAULT_CONFIG['default_mode']))
        tk.Radiobutton(mf, text=t('settings.mode_ratio'), variable=self.mode_var,
                      value='ratio', bg='white', font=('Microsoft YaHei', 9),
                      activebackground='white', command=self._toggle_mode
                      ).pack(side='left', padx=(0, 12))
        tk.Radiobutton(mf, text=t('settings.mode_fixed'), variable=self.mode_var,
                      value='fixed', bg='white', font=('Microsoft YaHei', 9),
                      activebackground='white', command=self._toggle_mode).pack(side='left')

        # Ratio row
        self.ratio_row = tk.Frame(frame, bg='white')
        self.ratio_row.pack(fill='x', pady=3)
        tk.Label(self.ratio_row, text=t('settings.default_ratio'), fg='#333', bg='white',
                font=('Microsoft YaHei', 10), width=14, anchor='w').pack(side='left')
        self.ratio_var = tk.StringVar(value=self.config.get('default_ratio', DEFAULT_CONFIG['default_ratio']))
        rm = tk.OptionMenu(self.ratio_row, self.ratio_var,
                          *ratio_options(self.ratio_var.get()))
        rm.configure(bg='#f0f0f0', font=('Microsoft YaHei', 9), relief='flat')
        rm.pack(side='left')

        # Fixed row
        self.fixed_row = tk.Frame(frame, bg='white')
        tk.Label(self.fixed_row, text=t('settings.fixed_size'), fg='#333', bg='white',
                font=('Microsoft YaHei', 10), width=14, anchor='w').pack(side='left')
        self.fw_var = tk.StringVar(value=self.config.get('fixed_width_str', DEFAULT_CONFIG['fixed_width_str']))
        self.fh_var = tk.StringVar(value=self.config.get('fixed_height_str', DEFAULT_CONFIG['fixed_height_str']))
        tk.Label(self.fixed_row, text=t('overlay.width'), fg='#666', bg='white',
                font=('Microsoft YaHei', 9)).pack(side='left')
        tk.Entry(self.fixed_row, textvariable=self.fw_var, width=8, bg='#f0f0f0',
                font=('Microsoft YaHei', 9)).pack(side='left', padx=3)
        tk.Label(self.fixed_row, text=t('overlay.height'), fg='#666', bg='white',
                font=('Microsoft YaHei', 9)).pack(side='left')
        tk.Entry(self.fixed_row, textvariable=self.fh_var, width=8, bg='#f0f0f0',
                font=('Microsoft YaHei', 9)).pack(side='left', padx=3)
        tk.Label(self.fixed_row, text=t('overlay.unit_hint'), fg='#999', bg='white',
                font=('Microsoft YaHei', 8)).pack(side='left', padx=(6, 0))

        if self.config.get('default_mode') == 'fixed':
            self.ratio_row.pack_forget()
            self.fixed_row.pack(fill='x', pady=3)
        else:
            self.fixed_row.pack_forget()

        # File format
        row = tk.Frame(frame, bg='white'); row.pack(fill='x', pady=3)
        tk.Label(row, text=t('settings.file_format'), fg='#333', bg='white',
                font=('Microsoft YaHei', 10), width=14, anchor='w').pack(side='left')
        self.fmt_var = tk.StringVar(value=self.config.get('file_format', DEFAULT_CONFIG['file_format']))
        fm = tk.OptionMenu(row, self.fmt_var, 'png', 'jpg', 'bmp')
        fm.configure(bg='#f0f0f0', font=('Microsoft YaHei', 9), relief='flat')
        fm.pack(side='left')

        # GIF format
        row = tk.Frame(frame, bg='white'); row.pack(fill='x', pady=3)
        tk.Label(row, text=t('gif.format'), fg='#333', bg='white',
                font=('Microsoft YaHei', 10), width=14, anchor='w').pack(side='left')
        self.gif_fmt_var = tk.StringVar(value=self.config.get('gif_format', DEFAULT_CONFIG['gif_format']))
        gfm = tk.OptionMenu(row, self.gif_fmt_var, 'gif', 'apng', 'webp')
        gfm.configure(bg='#f0f0f0', font=('Microsoft YaHei', 9), relief='flat')
        gfm.pack(side='left')
        tk.Label(row, text='GIF/APNG/WebP', fg='#999', bg='white',
                font=('Microsoft YaHei', 8)).pack(side='left', padx=(8, 0))

        # File prefix
        row = tk.Frame(frame, bg='white'); row.pack(fill='x', pady=3)
        tk.Label(row, text=t('settings.file_prefix'), fg='#333', bg='white',
                font=('Microsoft YaHei', 10), width=14, anchor='w').pack(side='left')
        self.pf_var = tk.StringVar(value=self.config.get('file_prefix', DEFAULT_CONFIG['file_prefix']))
        tk.Entry(row, textvariable=self.pf_var, width=20, bg='#f0f0f0',
                font=('Microsoft YaHei', 9)).pack(side='left')

        # Language
        row = tk.Frame(frame, bg='white'); row.pack(fill='x', pady=3)
        tk.Label(row, text=t('settings.language'), fg='#333', bg='white',
                font=('Microsoft YaHei', 10), width=14, anchor='w').pack(side='left')
        self.lang_var = tk.StringVar(value=self.config.get('language', DEFAULT_CONFIG['language']))
        lm = tk.OptionMenu(row, self.lang_var, 'zh', 'en')
        lm.configure(bg='#f0f0f0', font=('Microsoft YaHei', 9), relief='flat')
        lm.pack(side='left')
        tk.Label(row, text=t('settings.lang_restart'), fg='#e67e22', bg='white',
                font=('Microsoft YaHei', 8)).pack(side='left', padx=(8, 0))

        # Options
        row = tk.Frame(frame, bg='white'); row.pack(fill='x', pady=3)
        tk.Label(row, text='', width=14, bg='white').pack(side='left')
        self.as_var = tk.BooleanVar(value=self.config.get('auto_save', DEFAULT_CONFIG['auto_save']))
        self.ac_var = tk.BooleanVar(value=self.config.get('auto_clipboard', DEFAULT_CONFIG['auto_clipboard']))
        tk.Checkbutton(row, text=t('settings.auto_save'), variable=self.as_var,
                      bg='white', font=('Microsoft YaHei', 9),
                      activebackground='white').pack(side='left')
        tk.Checkbutton(row, text=t('settings.auto_clipboard'), variable=self.ac_var,
                      bg='white', font=('Microsoft YaHei', 9),
                      activebackground='white').pack(side='left', padx=(12, 0))

        # Buttons
        row = tk.Frame(frame, bg='white'); row.pack(fill='x', pady=(18, 0))
        tk.Button(row, text=t('settings.save_btn'), command=self._save,
                 bg='#27ae60', fg='white', font=('Microsoft YaHei', 10),
                 relief='flat', cursor='hand2', padx=20, pady=5
                 ).pack(side='right', padx=(6, 0))
        tk.Button(row, text=t('settings.cancel'), command=self.root.destroy,
                 bg='#ddd', fg='#333', font=('Microsoft YaHei', 10),
                 relief='flat', cursor='hand2', padx=16, pady=5).pack(side='right')

    def _toggle_mode(self):
        if self.mode_var.get() == 'fixed':
            self.fixed_row.pack(fill='x', pady=3)
            self.ratio_row.pack_forget()
        else:
            self.ratio_row.pack(fill='x', pady=3)
            self.fixed_row.pack_forget()

    def _browse_dir(self):
        path = filedialog.askdirectory(title='Select save directory')
        if path:
            self.dir_var.set(path)

    def _save(self):
        from dimensions import parse_dimension

        hotkey, hotkey_error = validate(self.hk_var.get().strip(), require_modifier=True)
        if hotkey_error:
            messagebox.showwarning('Error', '快捷键无效：' + hotkey_error)
            return

        w_str = self.fw_var.get().strip()
        h_str = self.fh_var.get().strip()
        try:
            fw = parse_dimension(w_str)
            fh = parse_dimension(h_str)
            if fw < 1 or fh < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning('Error', self.t('settings.dim_error'))
            return

        # Refresh from the central store before writing so this legacy
        # compatibility window cannot overwrite newer web/overlay fields.
        cfg = {
            **load_config(),
            'hotkey': hotkey,
            'default_mode': self.mode_var.get(),
            'default_ratio': self.ratio_var.get(),
            'fixed_width_str': w_str, 'fixed_height_str': h_str,
            'fixed_width': fw, 'fixed_height': fh,
            'save_directory': self.dir_var.get().strip(),
            'auto_save': self.as_var.get(),
            'auto_clipboard': self.ac_var.get(),
            'file_format': self.fmt_var.get(),
            'file_prefix': self.pf_var.get().strip() or 'screenshot_',
            'language': self.lang_var.get(),
            'gif_format': self.gif_fmt_var.get(),
        }
        save_config(cfg)
        messagebox.showinfo('OK', self.t('settings.saved'))
        self.root.destroy()


def run_settings():
    w = SettingsWindow()
    w.run()


if __name__ == '__main__':
    run_settings()
