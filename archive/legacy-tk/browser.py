#!/usr/bin/env python3
"""
drawru-imgter — 内置图片浏览器
浏览截图目录中的图片和 GIF 动图，支持缩略图网格和全屏预览
"""

import os, platform
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading


class ImageBrowser:
    """图片/GIF 浏览器窗口。"""

    def __init__(self, save_dir):
        self.save_dir = save_dir
        self.root = None
        self.canvas = None
        self.thumb_frame = None
        self.status_label = None
        self.files = []
        self.thumbs = {}          # filepath → PhotoImage
        self.thumb_labels = {}    # filepath → Label widget
        self.current_idx = -1
        self.preview_win = None
        self.gif_playing = False
        self.gif_frames = []
        self.gif_delay = 100
        self.gif_idx = 0
        self._mousewheel_binding = None

    def run(self):
        self.root = tk.Toplevel()
        self.root.title('drawru-imgter — 图片浏览器')
        self.root.configure(bg='#1e1e1e')
        self.root.geometry('900x620')
        self.root.minsize(600, 400)

        # 居中
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w, h = 900, 620
        self.root.geometry(f'+{(sw-w)//2}+{(sh-h)//2}')

        self._build_ui()
        self._load_files()
        self.root.bind('<Escape>', lambda e: self.close())
        self.root.protocol('WM_DELETE_WINDOW', self.close)

    def close(self):
        if self._mousewheel_binding is not None:
            try:
                self.root.unbind_all('<MouseWheel>')
            except tk.TclError:
                pass
            self._mousewheel_binding = None
        if self.preview_win and self.preview_win.winfo_exists():
            self.preview_win.destroy()
            self.preview_win = None
        if self.root and self.root.winfo_exists():
            self.root.destroy()

    def _build_ui(self):
        # 顶部工具栏
        toolbar = tk.Frame(self.root, bg='#2d2d2d', height=40)
        toolbar.pack(fill='x')
        toolbar.pack_propagate(False)

        tk.Label(toolbar, text='🖼 图片浏览器', fg='white', bg='#2d2d2d',
                font=('Microsoft YaHei', 11, 'bold')).pack(side='left', padx=12)

        self.status_label = tk.Label(toolbar, text='', fg='#999', bg='#2d2d2d',
                                     font=('Microsoft YaHei', 9))
        self.status_label.pack(side='right', padx=12)

        refresh_btn = tk.Button(toolbar, text='刷新', command=self._load_files,
                               bg='#3c3c3c', fg='white', font=('Microsoft YaHei', 9),
                               relief='flat', cursor='hand2', padx=10)
        refresh_btn.pack(side='right', padx=(0, 8), pady=6)

        close_btn = tk.Button(toolbar, text='✕', command=self.close,
                             bg='#3c3c3c', fg='white', font=('Microsoft YaHei', 9, 'bold'),
                             relief='flat', cursor='hand2', padx=10)
        close_btn.pack(side='right', pady=6)

        explorer_btn = tk.Button(toolbar, text='打开目录', command=self._open_dir,
                                bg='#3c3c3c', fg='white', font=('Microsoft YaHei', 9),
                                relief='flat', cursor='hand2', padx=10)
        explorer_btn.pack(side='right', pady=6)

        # 缩略图滚动区域
        container = tk.Frame(self.root, bg='#1e1e1e')
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bg='#1e1e1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        self.thumb_frame = tk.Frame(canvas, bg='#1e1e1e')
        self.thumb_frame.bind('<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.create_window((0, 0), window=self.thumb_frame, anchor='nw', tags='inner')
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        # 鼠标滚轮滚动
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * event.delta / 120), 'units')

        self._mousewheel_binding = canvas.bind_all('<MouseWheel>', _on_mousewheel)
        self._thumb_canvas = canvas

    def _load_files(self):
        """加载截图目录中的所有图片文件。"""
        for widget in self.thumb_frame.winfo_children():
            widget.destroy()
        self.files = []
        self.thumbs = {}
        self.thumb_labels = {}

        if not os.path.isdir(self.save_dir):
            self.status_label.config(text='目录不存在')
            return

        exts = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'}
        files = []
        for f in os.listdir(self.save_dir):
            ext = os.path.splitext(f)[1].lower()
            if ext in exts:
                files.append(os.path.join(self.save_dir, f))

        files.sort(key=os.path.getmtime, reverse=True)
        self.files = files
        self.status_label.config(text=f'{len(files)} 个文件')
        self._build_thumbnails()

    def _build_thumbnails(self):
        """构建缩略图网格。"""
        THUMB_SIZE = 160
        COLS = max(1, (self.root.winfo_width() - 40) // (THUMB_SIZE + 16))

        row = col = 0
        for i, filepath in enumerate(self.files):
            try:
                img = Image.open(filepath)
                img.thumbnail((THUMB_SIZE, THUMB_SIZE), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.thumbs[filepath] = photo
            except Exception:
                continue

            # 缩略图卡片
            card = tk.Frame(self.thumb_frame, bg='#2d2d2d',
                           highlightthickness=0, cursor='hand2')
            card.grid(row=row, column=col, padx=6, pady=6)

            lbl = tk.Label(card, image=photo, bg='#2d2d2d')
            lbl.pack(padx=1, pady=(1, 0))

            # 文件名 + 类型标签
            fname = os.path.basename(filepath)
            ext = os.path.splitext(fname)[1].lower()
            is_gif = ext == '.gif'

            name_lbl = tk.Label(card, text=fname[:22], fg='#ccc', bg='#2d2d2d',
                               font=('Microsoft YaHei', 8), anchor='w')
            name_lbl.pack(fill='x', padx=4, pady=(2, 0))

            if is_gif:
                gif_tag = tk.Label(card, text='GIF', fg='white', bg='#e74c3c',
                                  font=('Microsoft YaHei', 7, 'bold'), padx=4)
                gif_tag.pack(side='bottom', anchor='e', padx=2, pady=2)

            # 点击事件
            idx = i
            for w in (card, lbl, name_lbl):
                w.bind('<Button-1>', lambda e, i=idx: self._open_preview(i))
                w.bind('<Double-Button-1>', lambda e, i=idx: self._open_preview(i))

            self.thumb_labels[filepath] = card
            col += 1
            if col >= COLS:
                col = 0
                row += 1

    def _open_preview(self, idx):
        """打开大图预览。"""
        if idx < 0 or idx >= len(self.files):
            return
        self.current_idx = idx

        filepath = self.files[idx]
        ext = os.path.splitext(filepath)[1].lower()

        # 销毁旧预览窗口
        if self.preview_win and self.preview_win.winfo_exists():
            self.preview_win.destroy()

        self.preview_win = tk.Toplevel(self.root)
        self.preview_win.title(f'预览 — {os.path.basename(filepath)}')
        self.preview_win.configure(bg='black')

        sw = self.preview_win.winfo_screenwidth()
        sh = self.preview_win.winfo_screenheight()
        w = min(sw - 80, 1200)
        h = sh - 80
        self.preview_win.geometry(f'{w}x{h}+{(sw-w)//2}+{(sh-h)//2}')

        # 为 GIF 先在打开时预加载所有帧
        self.gif_frames = []
        self.gif_delay = 100
        self.gif_idx = 0
        self.gif_playing = ext == '.gif'

        def load_and_show():
            try:
                img = Image.open(filepath)
                if ext == '.gif':
                    # 提取所有帧
                    for frame in ImageSequence.Iterator(img):
                        self.gif_frames.append(frame.copy().convert('RGBA'))
                    # 获取帧延迟
                    try:
                        self.gif_delay = img.info.get('duration', 100)
                        self.gif_delay = max(20, int(self.gif_delay or 20))
                    except Exception:
                        self.gif_delay = 100
                    self.preview_win.after(0, self._show_gif_frame)
                else:
                    # Pillow 解码可在线程执行，但 Tk 控件只能在主线程创建/更新。
                    self.preview_win.after(0, lambda: self._show_static(img, filepath))
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(text=f'打开失败: {e}'))

        threading.Thread(target=load_and_show, daemon=True).start()

        # 键盘导航
        self.preview_win.bind('<Escape>', lambda e: self.preview_win.destroy())
        self.preview_win.bind('<Left>', lambda e: self._navigate(-1))
        self.preview_win.bind('<Right>', lambda e: self._navigate(1))
        self.preview_win.bind('<Delete>', lambda e: self._delete_current())

    def _show_static(self, img, filepath):
        il = tk.Label(self.preview_win, bg='black')
        il.pack(fill='both', expand=True)

        pw = self.preview_win.winfo_width()
        ph = self.preview_win.winfo_height()
        if pw < 100:
            pw, ph = 800, 600

        scale = min(pw / img.width, ph / img.height)
        nw = int(img.width * scale)
        nh = int(img.height * scale)
        img_resized = img.resize((nw, nh), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img_resized)

        il.configure(image=photo)
        il.image = photo  # 防 GC

        # 底部信息栏
        self._build_info_bar(
            f'{os.path.basename(filepath)}   {img.width}×{img.height}   {os.path.getsize(filepath)//1024} KB'
        )

    def _show_gif_frame(self):
        if not self.preview_win or not self.preview_win.winfo_exists():
            return
        if not self.gif_frames:
            return

        il = tk.Label(self.preview_win, bg='black')
        il.pack(fill='both', expand=True)

        def update_frame():
            if not self.gif_playing or not self.preview_win or not self.preview_win.winfo_exists():
                return
            frame = self.gif_frames[self.gif_idx % len(self.gif_frames)]

            pw = self.preview_win.winfo_width()
            ph = self.preview_win.winfo_height()
            if pw < 100:
                pw, ph = 800, 600

            scale = min(pw / frame.width, ph / frame.height)
            nw = max(1, int(frame.width * scale))
            nh = max(1, int(frame.height * scale))
            fr = frame.resize((nw, nh), Image.LANCZOS)
            photo = ImageTk.PhotoImage(fr)
            il.configure(image=photo)
            il.image = photo

            self.gif_idx += 1
            self.preview_win.after(self.gif_delay, update_frame)

        update_frame()

        filepath = self.files[self.current_idx]
        self._build_info_bar(
            f'GIF  {os.path.basename(filepath)}   {len(self.gif_frames)} 帧   {self.gif_delay}ms   {os.path.getsize(filepath)//1024} KB  |  ← → 切换  Space 暂停  Del 删除'
        )

        self.preview_win.bind('<space>', self._toggle_gif)

    def _toggle_gif(self, event=None):
        self.gif_playing = not self.gif_playing
        if self.gif_playing:
            self._show_gif_frame()

    def _navigate(self, delta):
        new_idx = self.current_idx + delta
        if 0 <= new_idx < len(self.files):
            self._open_preview(new_idx)

    def _delete_current(self):
        """删除当前预览的图片。"""
        if self.current_idx < 0 or self.current_idx >= len(self.files):
            return
        filepath = self.files[self.current_idx]
        if not os.path.exists(filepath):
            return

        # 确认
        from tkinter import messagebox
        fname = os.path.basename(filepath)
        if not messagebox.askyesno('确认删除', f'确定要删除 {fname} 吗？'):
            return

        os.remove(filepath)
        self.files.pop(self.current_idx)
        self.status_label.config(text=f'已删除 {fname}')

        if self.preview_win:
            self.preview_win.destroy()
            self.preview_win = None

        # 刷新缩略图
        self._load_files()

    def _build_info_bar(self, text):
        """预览窗口底部信息栏。"""
        # 移除旧信息栏
        for w in self.preview_win.winfo_children():
            if hasattr(w, '_is_info_bar'):
                w.destroy()

        bar = tk.Frame(self.preview_win, bg='#000000aa', height=30)
        bar._is_info_bar = True
        bar.pack(side='bottom', fill='x')
        bar.pack_propagate(False)

        tk.Label(bar, text=text, fg='white', bg='#00000000',
                font=('Consolas', 9)).pack(side='left', padx=12, pady=4)

    def _open_dir(self):
        """在资源管理器中打开截图目录。"""
        import subprocess
        if os.name == 'nt':
            subprocess.Popen(['explorer', self.save_dir])
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', self.save_dir])
        else:
            subprocess.Popen(['xdg-open', self.save_dir])


def run_browser(save_dir):
    """独立运行浏览器（需要已有 tk root）。"""
    browser = ImageBrowser(save_dir)
    browser.run()
    return browser
