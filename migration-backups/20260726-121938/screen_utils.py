"""Compatibility alias for the v5 screen services."""
import importlib, sys
import _src_bootstrap
sys.modules[__name__] = importlib.import_module('xaocen_imgtor.screen_utils')
