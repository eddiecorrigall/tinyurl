#!/bin/bash

set -e

# Run tests first
sh bin/test.sh

# Deploy
SLS_DEBUG=true \
	serverless deploy
