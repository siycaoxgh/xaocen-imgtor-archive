# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['webapp.py'],
    pathex=['.', 'src'],
    binaries=[],
    datas=[('ui', 'ui'), ('main.py', '.'), ('gifrecorder_standalone.py', '.'), ('video_recorder_standalone.py', '.'), ('xaocen-imgtor.ico', '.')],
    # Worker entry points are bundled as data and executed through runpy, so
    # PyInstaller cannot discover their imports from webapp.py automatically.
    hiddenimports=[
        'screen_utils', 'overlay', 'gifrecorder', 'native_toolbar',
        'rounded_controls', 'design_tokens', 'config_manager', 'instance_lock',
        'shortcuts', 'ratio_presets', 'presets', 'dimensions', 'i18n',
        'clipboard_utils', 'app_log', 'runtime_status', 'video_plugin_runtime',
        'pynput.keyboard', 'pynput.keyboard._win32',
        'xaocen_imgtor',
        'xaocen_imgtor.app_log', 'xaocen_imgtor.clipboard_utils',
        'xaocen_imgtor.config_manager', 'xaocen_imgtor.design_tokens',
        'xaocen_imgtor.dimensions', 'xaocen_imgtor.i18n',
        'xaocen_imgtor.instance_lock', 'xaocen_imgtor.native_toolbar',
        'xaocen_imgtor.plugin_host', 'xaocen_imgtor.plugin_manager',
        'xaocen_imgtor.plugin_packager', 'xaocen_imgtor.presets',
        'xaocen_imgtor.ratio_presets', 'xaocen_imgtor.rounded_controls',
        'xaocen_imgtor.runtime_status', 'xaocen_imgtor.screen_utils',
        'xaocen_imgtor.shortcuts', 'xaocen_imgtor.tray',
        'xaocen_imgtor.video_plugin_runtime',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='XAOCEN-ImgTor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['xaocen-imgtor.ico'],
)
