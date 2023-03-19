#!/bin/bash

# Create a "python" directory
mkdir python

# Install the dependencies into the "python" directory
pip install -r requirements.txt -t python/

# Create a zip file named "requirements.zip" with the "python" directory
zip -r requirements.zip python

# Remove the "python" directory
rm -rf python
