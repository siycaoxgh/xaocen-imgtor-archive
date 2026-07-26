"""Compatibility alias for the v5 runtime status service."""
import importlib, sys
import _src_bootstrap
sys.modules[__name__] = importlib.import_module('xaocen_imgtor.runtime_status')
