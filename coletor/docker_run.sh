#!/bin/bash

./docker_stop.sh

echo "iniciando o serviço Coletor..."

docker run --name coletor -e DATABASE_URL="postgresql+psycopg2://postgres:postgres@192.168.68.111:5432/cys_core" \
-e SECRET_KEY="your-production-secret-key" -e DB_DEFAULT_FORMAT_DATE="%Y-%m-%d %H:%M:%S" -p 8000:8000 coletor:latest

docker ps