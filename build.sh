#!/bin/bash

# Navigate to the uvx-node directory
cd uvx-node || exit

# Build the Docker image
docker build -t mcporbit/node-runner .