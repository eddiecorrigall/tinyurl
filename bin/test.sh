#!/bin/bash

set -e

export PYTHONPATH
PYTHONPATH="$(pwd)"
export FLASK_CONFIG='testing'
export FLASK_DEBUG=1

py.test "$@" tests/
