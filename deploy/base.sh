#!/bin/bash
cd  ..
docker build -f deploy/Dockerfile_base -t docker.kexie.space/wilinz/paddlepaddle-base:latest --push .
