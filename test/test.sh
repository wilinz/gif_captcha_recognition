#!/bin/bash

ab -n 1000 -c 10 -p post_data.txt -T 'application/x-www-form-urlencoded' http://172.16.0.209:5000/ocr