#!/bin/bash

set -e

# De-provision custom domain mapping
SLS_DEBUG=* \
    serverless delete_domain --verbose "$@"

# De-provision app
SLS_DEBUG=* \
    serverless remove --verbose "$@"
