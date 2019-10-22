#!/bin/bash

set -e

# Bootstrap project

if [ -z "$(command -v node)" ]; then
    brew install node
fi

if [ -z "$(command -v serverless)" ]; then
    npm install -g serverless
fi

# Install node requirements
npm install

# Install python requirements
python3.7 -m venv venv
. venv/bin/activate
pip3 install --upgrade pip
pip3 install --upgrade setuptools
pip3 install --requirement requirements.txt

# Install Redis Server
# brew install redis
# brew upgrade redis
# brew services start redis

