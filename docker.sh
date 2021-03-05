#!/bin/bash
docker build -t latest . && docker run --name python-mint --env-file ./env.properties latest 