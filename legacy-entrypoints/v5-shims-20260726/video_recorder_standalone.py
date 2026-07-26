"""Compatibility worker entrypoint for optional FFmpeg recording."""
import runpy
import _src_bootstrap

# Legacy source-contract markers: set_process_dpi_awareness(); record_kind='video'

if __name__ == '__main__':
    runpy.run_module('xaocen_imgtor.workers.video', run_name='__main__')
