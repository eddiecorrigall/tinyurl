#!/bin/bash

set -e

. ./venv/bin/activate

export PYTHONPATH
PYTHONPATH="$(pwd)"
export FLASK_CONFIG='testing'
export FLASK_DEBUG=1

TINYURL_SECRET_KEY='superman' \
	pytest "$@" tests/
