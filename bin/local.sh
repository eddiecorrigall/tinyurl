#!/bin/bash

set -e

. venv/bin/activate

# Run locally
TINYURL_SECRET_KEY=superman \
FLASK_DEBUG=1 \
    serverless wsgi serve
