"""Compatibility alias for the v5 screenshot engine."""
import importlib
import sys
import _src_bootstrap

sys.modules[__name__] = importlib.import_module('xaocen_imgtor.overlay')
