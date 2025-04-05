
@echo off

REM Navigate to the uvx-node directory
cd /d "uvx-node" || exit /b

REM Build the Docker image
docker build -t mcporbit/node-runner .