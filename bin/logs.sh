#!/bin/bash

set -e

# Get logs
serverless logs --function app "$@"
