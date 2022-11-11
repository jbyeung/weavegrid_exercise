#!/bin/bash
app="docker.weavegrid_exercise"
docker build -t ${app} .
docker run -d -p 56733:80 \
  --platform linux/amd64 \
  --name=${app} \
  -v $PWD:/app ${app}
