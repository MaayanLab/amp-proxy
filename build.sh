#!/usr/bin/env bash

img=maayanlab/maayanlab-haproxy

docker build --no-cache -t $img .
docker push $img
