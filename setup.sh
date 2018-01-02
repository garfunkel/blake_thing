#!/bin/bash

# Create virtual environment
python3.6 -m virtualenv venv

if [ $? -ne 0 ]; then
    >&2 echo "Failed to install virtual environment."

    exit 1
fi

# Add environment variables to source script thing
echo -e "\n\n# Flask Stuffs\nexport PYTHONPATH=$PWD\nexport FLASK_APP=blake.py" >> venv/bin/activate

# Install pip requirements
$PWD/venv/bin/pip install -r requirements.txt

if [ $? -ne 0 ]; then
    >&2 echo "Failed to install python packages."

    exit 1
fi

# Install bower packages
bower install

if [ $? -ne 0 ]; then
    >&2 echo "Failed to install bower packages."

    exit 1
fi

# Install redis
curl -O http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
rm redis-stable.tar.gz
cd redis-stable
make

if [ $? -ne 0 ]; then
    >&2 echo "Failed to build redis."

    exit 1
fi
