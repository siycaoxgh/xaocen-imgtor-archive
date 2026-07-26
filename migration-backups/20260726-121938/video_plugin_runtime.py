"""Compatibility alias for the v5 video plugin runtime."""
import importlib, sys
import _src_bootstrap
sys.modules[__name__] = importlib.import_module('xaocen_imgtor.video_plugin_runtime')
