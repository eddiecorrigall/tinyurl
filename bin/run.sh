#!/bin/bash

set -e

# Test first
sh bin/test.sh

# Run locally
serverless wsgi serve
