#!/bin/bash

docker run -d --name rum-agent -p 9090:80 rum-agent:latest

docker ps | grep rum-agent