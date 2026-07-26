"""Compatibility alias for the v5 translations."""
import importlib, sys
import _src_bootstrap
sys.modules[__name__] = importlib.import_module('xaocen_imgtor.i18n')
