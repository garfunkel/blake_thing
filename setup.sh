#!/bin/bash

# Create virtual environment
python3.6 -m virtualenv venv

# Add environment variables to source script thing
echo -e "\n\n# Flask Stuffs\nexport PYTHONPATH=$PWD\nexport FLASK_APP=blake.py" >> venv/bin/activate

# Install pip requirements
$PWD/venv/bin/pip install -r requirements.txt

# Install bower packages
bower install

# Install redis
curl -O http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
rm redis-stable.tar.gz
cd redis-stable
make

