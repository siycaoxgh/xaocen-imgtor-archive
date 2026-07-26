#!/usr/bin/env python3
"""
drawru-imgter — 图片裁剪工具
打开已有图片，拖框裁剪并保存
"""

import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from ratio_presets import RATIO_PRESETS


def canvas_rect_to_image(start_x, start_y, end_x, end_y,
                         image_x, image_y, scale, image_width, image_height):
    """Convert canvas coordinates to a clamped rectangle in the source image."""
    x1 = int((min(start_x, end_x) - image_x) / scale)
    y1 = int((min(start_y, end_y) - image_y) / scale)
    x2 = int((max(start_x, end_x) - image_x) / scale)
    y2 = int((max(start_y, end_y) - image_y) / scale)
    return (
        max(0, min(image_width, x1)),
        max(0, min(image_height, y1)),
        max(0, min(image_width, x2)),
        max(0, min(image_height, y2)),
    )


class ImageCropper:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.img = None          # 原始 PIL Image
        self.tk_img = None       # PhotoImage
        self.filepath = None
        self.start_x = self.start_y = 0
        self.current_x = self.current_y = 0
        self.scale = 1.0
        self.image_x = self.image_y = 0
        self.image_w = self.image_h = 0
        self.status_label = None
        self.constraint_var = None
        self.crop_w_var = None
        self.crop_h_var = None

    def run(self):
        self.root = tk.Toplevel()
        self.root.title('drawru-imgter — 图片裁剪')
        self.root.configure(bg='#1e1e1e')
        self.root.geometry('900x620')

        self._build_ui()

        # 先弹文件选择
        self.root.after(100, self._open_file)

    def _build_ui(self):
        toolbar = tk.Frame(self.root, bg='#2d2d2d', height=40)
        toolbar.pack(fill='x')
        toolbar.pack_propagate(False)

        tk.Label(toolbar, text='✂ 图片裁剪', fg='white', bg='#2d2d2d',
                font=('Microsoft YaHei', 11, 'bold')).pack(side='left', padx=12)

        tk.Button(toolbar, text='打开图片', command=self._open_file,
                 bg='#3c3c3c', fg='white', font=('Microsoft YaHei', 9),
                 relief='flat', cursor='hand2', padx=10).pack(side='left', padx=4)

        tk.Button(toolbar, text='裁剪并保存', command=self._crop_save,
                 bg='#27ae60', fg='white', font=('Microsoft YaHei', 9),
                  relief='flat', cursor='hand2', padx=12).pack(side='left', padx=4)

        tk.Label(toolbar, text='比例', fg='#ccc', bg='#2d2d2d').pack(side='left', padx=(12, 3))
        self.constraint_var = tk.StringVar(value='free')
        tk.OptionMenu(toolbar, self.constraint_var, 'free', *RATIO_PRESETS, 'fixed').pack(side='left')
        self.crop_w_var = tk.StringVar(value='400')
        self.crop_h_var = tk.StringVar(value='320')
        tk.Entry(toolbar, textvariable=self.crop_w_var, width=5, bg='#3c3c3c', fg='white', relief='flat').pack(side='left', padx=2)
        tk.Label(toolbar, text='×', fg='#ccc', bg='#2d2d2d').pack(side='left')
        tk.Entry(toolbar, textvariable=self.crop_h_var, width=5, bg='#3c3c3c', fg='white', relief='flat').pack(side='left', padx=2)

        self.status_label = tk.Label(toolbar, text='', fg='#999', bg='#2d2d2d',
                                     font=('Microsoft YaHei', 9))
        self.status_label.pack(side='right', padx=12)

        # Canvas
        self.canvas = tk.Canvas(self.root, bg='#1e1e1e', highlightthickness=0,
                                cursor='crosshair')
        self.canvas.pack(fill='both', expand=True)

        self.canvas.bind('<ButtonPress-1>', self._on_press)
        self.canvas.bind('<B1-Motion>', self._on_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_release)
        self.root.bind('<Escape>', lambda e: self.root.destroy())

    def _open_file(self):
        path = filedialog.askopenfilename(
            title='选择要裁剪的图片',
            filetypes=[('Image files', '*.png *.jpg *.jpeg *.bmp *.gif *.webp'),
                      ('All files', '*.*')]
        )
        if not path:
            return

        self.filepath = path
        self.img = Image.open(path)

        # 缩放到窗口
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 100:
            w, h = 800, 600

        scale = min(w / self.img.width, h / self.img.height, 1.0)
        self.scale = scale
        nw = int(self.img.width * scale)
        nh = int(self.img.height * scale)
        self.image_w, self.image_h = nw, nh
        self.image_x = (w - nw) // 2
        self.image_y = (h - nh) // 2

        img_resized = self.img.resize((nw, nh), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img_resized)

        self.canvas.delete('all')
        self.canvas.create_image(self.image_x, self.image_y, image=self.tk_img, anchor='nw')

        self.status_label.config(
            text=f'{os.path.basename(path)}  {self.img.width}×{self.img.height}'
        )

    def _on_press(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.start_x = max(self.image_x, min(self.image_x + self.image_w, x))
        self.start_y = max(self.image_y, min(self.image_y + self.image_h, y))
        self.canvas.delete('cropbox')

    def _on_drag(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.current_x = max(self.image_x, min(self.image_x + self.image_w, x))
        self.current_y = max(self.image_y, min(self.image_y + self.image_h, y))
        self._apply_constraint()
        self._draw_box()

    def _on_release(self, event):
        if self.img is None or self.scale <= 0:
            return
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.current_x = max(self.image_x, min(self.image_x + self.image_w, x))
        self.current_y = max(self.image_y, min(self.image_y + self.image_h, y))
        self._apply_constraint()
        self._draw_box()

        # 计算原始图片坐标
        x1, y1, x2, y2 = canvas_rect_to_image(
            self.start_x, self.start_y, self.current_x, self.current_y,
            self.image_x, self.image_y, self.scale, self.img.width, self.img.height)

        cw = x2 - x1
        ch = y2 - y1
        if cw > 2 and ch > 2:
            self.status_label.config(text=f'选区: {x1},{y1} → {x2},{y2}  ({cw}×{ch}) | 点击"裁剪并保存"')

    def _draw_box(self):
        self.canvas.delete('cropbox')
        self.canvas.create_rectangle(
            self.start_x, self.start_y, self.current_x, self.current_y,
            outline='#00d4ff', width=2, tags='cropbox'
        )
        # 虚线辅助
        self.canvas.create_line(
            self.start_x, self.start_y, self.current_x, self.current_y,
            fill='#00d4ff', dash=(4, 4), width=1, tags='cropbox'
        )

    def _apply_constraint(self):
        mode = self.constraint_var.get() if self.constraint_var else 'free'
        w = abs(self.current_x - self.start_x)
        if mode == 'fixed':
            try:
                target_w = max(1, float(self.crop_w_var.get())) * self.scale
                target_h = max(1, float(self.crop_h_var.get())) * self.scale
            except (ValueError, ZeroDivisionError):
                target_w, target_h = 400 * self.scale, 320 * self.scale
            sign_x = 1 if self.current_x >= self.start_x else -1
            sign_y = 1 if self.current_y >= self.start_y else -1
            self.current_x = self.start_x + sign_x * target_w
            self.current_y = self.start_y + sign_y * target_h
            self.current_x = max(self.image_x, min(self.image_x + self.image_w, self.current_x))
            self.current_y = max(self.image_y, min(self.image_y + self.image_h, self.current_y))
            return
        elif mode != 'free':
            a, b = mode.split(':'); ratio = float(b) / float(a)
        else:
            return
        h = max(1, w * ratio)
        self.current_y = self.start_y + (h if self.current_y >= self.start_y else -h)
        self.current_y = max(self.image_y, min(self.image_y + self.image_h, self.current_y))
        self.canvas.create_line(
            self.current_x, self.start_y, self.start_x, self.current_y,
            fill='#00d4ff', dash=(4, 4), width=1, tags='cropbox'
        )

    def _crop_save(self):
        if not self.img:
            messagebox.showwarning('提示', '请先打开一张图片')
            return

        cw = int(abs(self.current_x - self.start_x) / self.scale)
        ch = int(abs(self.current_y - self.start_y) / self.scale)
        if cw < 3 or ch < 3:
            messagebox.showwarning('提示', '请先拖拽选择一个裁剪区域')
            return

        x1, y1, x2, y2 = canvas_rect_to_image(
            self.start_x, self.start_y, self.current_x, self.current_y,
            self.image_x, self.image_y, self.scale, self.img.width, self.img.height)

        cropped = self.img.crop((x1, y1, x2, y2))

        # 保存到原图目录
        base, ext = os.path.splitext(self.filepath)
        out_path = f'{base}_cropped{ext}'
        cropped.save(out_path)

        messagebox.showinfo('完成',
                           f'裁剪成功！\n已保存到:\n{out_path}\n尺寸: {cropped.width}×{cropped.height}')
        self.status_label.config(
            text=f'已保存: {os.path.basename(out_path)}  {cropped.width}×{cropped.height}'
        )


def run_cropper():
    c = ImageCropper()
    c.run()
