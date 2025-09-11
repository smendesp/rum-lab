#!/bin/bash

export VIRTUAL_ENV=$PWD/.venv

#export UV_ENV_FILE=./.env

export OTEL_SERVICE_NAME=coletor-rum
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_INSECURE=true
export OTEL_EXPORTER_OTLP_ENDPOINT=192.168.68.111:4317
export OTEL_TRACES_EXPORTER=otlp
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true

export OTEL_BSP_SCHEDULE_DELAY=5000
export OTEL_BSP_EXPORT_TIMEOUT=30000
export OTEL_BSP_MAX_QUEUE_SIZE=2048
export OTEL_BSP_MAX_EXPORT_BATCH_SIZE=512

export OTEL_PYTHON_LOG_CORRELATION=true
export OTEL_PYTHON_LOG_LEVEL=INFO

#source ./.env
#uv run fastapi dev 


uv run opentelemetry-instrument uvicorn app.main:app


#uv run uvicorn app.main:app