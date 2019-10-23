#!/bin/bash

set -e

. venv/bin/activate

# Test first
sh bin/test.sh

# Run locally
serverless wsgi serve
