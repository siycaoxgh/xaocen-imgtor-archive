"""Compatibility alias for the v5 plugin packager."""
import importlib, sys
import _src_bootstrap
sys.modules[__name__] = importlib.import_module('xaocen_imgtor.plugin_packager')
