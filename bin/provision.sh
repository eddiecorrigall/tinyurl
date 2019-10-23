#!/bin/bash

set -e

# Run tests first
sh bin/test.sh

# Provision custom domain mapping
serverless create_domain "$@"

# Deploy
serverless deploy "$@"
