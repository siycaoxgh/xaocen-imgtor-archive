"""Compatibility worker entrypoint for GIF/APNG/WebP recording."""
import runpy
import _src_bootstrap

if __name__ == '__main__':
    runpy.run_module('xaocen_imgtor.workers.gifrecorder', run_name='__main__')
