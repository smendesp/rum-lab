#! /bin/sh

echo "Starting Uvicorn with $WORKERS workers..."

opentelemetry-instrument uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers $WORKERS