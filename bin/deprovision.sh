#!/bin/bash

set -e

# De-provision custom domain mapping
serverless delete_domain "$@"

# De-provision app
serverless remove "$@"
