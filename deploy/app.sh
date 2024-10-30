#!/bin/bash
cd  ..
docker build -f deploy/Dockerfile -t docker.kexie.space/wilinz/captchasolve:latest --push .
