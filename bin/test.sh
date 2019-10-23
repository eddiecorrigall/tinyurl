#!/bin/bash

set -e

. ./venv/bin/activate

export PYTHONPATH
PYTHONPATH="$(pwd)"

TINYURL_SECRET_KEY='superman' \
FLASK_CONFIG='testing' \
FLASK_DEBUG=1 \
	pytest "$@" tests/
