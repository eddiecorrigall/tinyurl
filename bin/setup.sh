#!/bin/bash

set -e

# Bootstrap project
brew install node
npm install
npm install -g serverless
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt

# Install Redis Server
brew install redis
brew upgrade redis
brew services start redis
