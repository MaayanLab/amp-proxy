#!/usr/bin/env bash

img=maayanlab/maayanlab-haproxy

docker build -t $img .
docker run -it -p 80:80 -p 52496:52496 -e TZ=America/New_York $img
