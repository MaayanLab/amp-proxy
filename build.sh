#!/usr/bin/env bash

img=maayanlab/marathon-haproxy-webhook

docker build -t $img .
docker push $img
