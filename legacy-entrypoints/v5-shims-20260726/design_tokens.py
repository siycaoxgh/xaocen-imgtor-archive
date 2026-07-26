"""Compatibility alias for the v5 native UI design tokens."""
import importlib, sys
import _src_bootstrap
sys.modules[__name__] = importlib.import_module('xaocen_imgtor.design_tokens')
