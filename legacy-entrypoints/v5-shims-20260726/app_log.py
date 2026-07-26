"""Compatibility alias for the v5 shared logging service."""
import importlib
import sys
import _src_bootstrap
sys.modules[__name__] = importlib.import_module('xaocen_imgtor.app_log')
