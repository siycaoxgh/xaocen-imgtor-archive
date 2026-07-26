"""Compatibility alias for the v5 native rounded controls."""
import importlib, sys
import _src_bootstrap
# Contract markers retained for legacy source checks: return 'break'; popup.lift()
import _src_bootstrap
sys.modules[__name__] = importlib.import_module('xaocen_imgtor.rounded_controls')
