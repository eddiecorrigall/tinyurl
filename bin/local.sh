#!/bin/bash

set -e

. venv/bin/activate

# Test first
sh bin/test.sh

# Run locally
TINYURL_SECRET_KEY=superman \
FLASK_DEBUG=1 \
    serverless wsgi serve
