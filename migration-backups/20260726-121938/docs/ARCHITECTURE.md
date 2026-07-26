# XAOCEN ImgTor v5 架构约定

## 目标

v5 采用“核心包 + 根目录兼容入口”的迁移方式：核心实现逐步收拢到
`src/xaocen_imgtor/`，根目录暂时保留少量入口和兼容导入层，保证源码运行、旧快捷方式、独立 worker 与 PyInstaller 构建连续可用。

## 目录职责

```text
根目录
├── webapp.py                         主界面入口
├── main.py                           截图监听 worker
├── gifrecorder_standalone.py         动图 worker
├── video_recorder_standalone.py      视频 worker
├── 启动.bat                           Windows 源码启动入口
├── XAOCEN-ImgTor.spec                PyInstaller 构建入口
├── src/xaocen_imgtor/                共享服务与基础模块
├── ui/                               HTML/CSS/JS 界面
├── plugin_examples/                  插件源码示例
├── plugin_sdk/                       插件开发说明
├── tests/                            自动化测试
├── docs/                             项目与平台文档
└── archive/                          历史文件、运行日志和锁文件
```

## 迁移规则

- 新的共享逻辑只能放入 `src/xaocen_imgtor/`，不要再新增根目录业务模块。
- 根目录兼容模块只允许做导入转发，不应新增业务代码。
- worker 仍保留根目录入口，直到子进程协议迁移为 `python -m xaocen_imgtor.workers.<name>` 并完成打包回归。
- `config.json`、插件、日志、缓存和锁文件属于运行时数据，不进入源码包。
- `plugin_examples/` 不是运行时插件目录；实际插件安装位置由插件管理器决定。

## PyInstaller 规则

`XAOCEN-ImgTor.spec` 使用 `src` 作为 `pathex`，同时显式声明 worker 数据文件和包的隐藏导入。每次移动模块后，必须运行：

```bat
python -m unittest discover -s tests -q
node --check ui/app.js
pyinstaller XAOCEN-ImgTor.spec
```

## 后续阶段

1. 将 `overlay.py`、`gifrecorder.py` 和原生 UI helper 迁移到 `src/xaocen_imgtor/`。
2. 将 worker 入口改为薄适配层，统一参数解析和退出码。
3. 将插件、日志、构建和发布命令集中到明确的工具目录。
4. 删除兼容 shim 前，至少完成源码启动、单实例、托盘、快捷键、截图、录制和 PyInstaller 实机回归。
