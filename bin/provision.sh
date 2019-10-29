#!/bin/bash

set -e

# Run tests first
sh bin/test.sh

# Collect information
while [ -z "${TINYURL_DOMAIN}" ]; do
	read -p "Enter TINYURL_DOMAIN: " TINYURL_DOMAIN
	echo
	export TINYURL_DOMAIN="${TINYURL_DOMAIN}"
done
while [ -z "${TINYURL_SECRET_KEY}" ]; do
    read -s -p "Enter TINYURL_SECRET_KEY: " TINYURL_SECRET_KEY
    echo
    export TINYURL_SECRET_KEY="${TINYURL_SECRET_KEY}"
done

# Provision custom domain mapping
serverless create_domain "$@"

# Deploy
serverless deploy "$@"
