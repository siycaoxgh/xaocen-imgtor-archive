# 2026-07-26 项目整理记录

本次只移动文件，没有删除文件。

## 已归档

- `build/`：PyInstaller 中间构建缓存。
- `dist/`：重复/临时构建输出，包含旧的运行时锁文件。
- `release/android_motion_photo.xaocen-plugin`：与 `release/v5.0.0/` 重复的插件包。
- `release/video_recorder_ffmpeg.xaocen-plugin`：与 `release/v5.0.0/` 重复的插件包。
- 根目录、旧入口目录、旧 Tk 目录和运行时目录中的 `__pycache__/`：Python 字节码缓存。

## 仍保留在主目录

- `webapp.py`、`ui/`、`src/`：主程序运行链路。
- `main.py`、`gifrecorder_standalone.py`、`video_recorder_standalone.py`：PyInstaller 和源码启动仍引用的兼容 worker 入口。
- `plugin_examples/`、`plugin_sdk/`：插件源码与开发说明。
- `release/v5.0.0/`：当前带版本号的发布目录。
- `tests/`、`docs/`、`requirements*.txt`、`XAOCEN-ImgTor.spec`：测试、文档和构建所需文件。

当前 `release/v5.0.0/` 下的运行时锁文件没有移动，因为审查时仍检测到该版本程序进程正在运行。完全退出程序后，可单独清理/归档其中的 `archive/runtime/`，不要把锁文件带入发布包。
