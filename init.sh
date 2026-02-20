#!/bin/bash
# init.sh

echo "Building and starting Docker containers..."
docker-compose up -d --build

echo "Waiting for MongoDB and MinIO to initialize (15 seconds)..."
sleep 15

echo "Running initial ETL pipeline to load test data..."
docker exec -it etl-worker python src/main.py

echo "========================================="
echo "Initialization complete!"
echo "Analytics Dashboard available at: http://localhost:8501"
echo "Mongo Express available at: http://localhost:8081"
echo "MinIO Console available at: http://localhost:9001"
echo "========================================="