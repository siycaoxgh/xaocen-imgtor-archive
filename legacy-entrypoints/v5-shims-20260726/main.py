"""Compatibility worker entrypoint for screenshot capture."""
import runpy
import _src_bootstrap

if __name__ == '__main__':
    runpy.run_module('xaocen_imgtor.workers.screenshot', run_name='__main__')
