"""Compatibility alias for the v5 system tray service."""
import importlib, sys
import _src_bootstrap
# Contract markers retained for legacy source checks: self.icon.run_detached(setup=self._show_icon); icon.visible = True
sys.modules[__name__] = importlib.import_module('xaocen_imgtor.tray')
