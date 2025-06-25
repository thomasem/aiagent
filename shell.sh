#!/usr/bin/env bash

docker build -t aiagent-dev .
docker run -it --rm -v $(pwd):/aiagent aiagent-dev:latest
