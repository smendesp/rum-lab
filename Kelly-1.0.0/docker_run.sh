#!/bin/bash

./docker_stop.sh

docker run -d --name kelly -p 9081:80 kelly:latest

docker ps | grep kelly