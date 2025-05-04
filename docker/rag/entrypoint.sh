#!/bin/bash
set -e

echo "Running database migrations..."
cd /app/models/db_shemas/rag/   
alembic upgrade head
cd /app
echo "Starting FastAPI application..."
exec "$@"