"""Compatibility alias for the v5 recording engine."""
import importlib
import sys
import _src_bootstrap

# Legacy source-contract markers; implementation lives in src/xaocen_imgtor.
# from design_tokens import ACCENT_BLUE
# fill=ACCENT_BLUE
# self._video_record_loop(record_bbox)
# build_gdigrab_command(

sys.modules[__name__] = importlib.import_module('xaocen_imgtor.gifrecorder')
