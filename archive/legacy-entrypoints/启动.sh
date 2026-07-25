#!/usr/bin/env sh
set -eu
exec "${PYTHON:-python3}" "$(dirname "$0")/启动.py"
