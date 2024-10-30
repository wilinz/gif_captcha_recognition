#!/bin/bash
cd  ..
docker build -f deploy/Dockerfile_base_cuda -t docker.kexie.space/wilinz/paddlepaddle-base-cuda:latest --push .
