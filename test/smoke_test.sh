#!/bin/bash

BASE_URL="http://localhost:5000"

echo "Running smoke tests against $BASE_URL"
echo "Checking /health"

for i in {1..10}; do
  if curl -fsS "$BASE_URL/health" > /dev/null; then
    echo "Health check passed"
    exit 0
  fi
  echo "Waiting for app to be ready..."
  sleep 2
done

echo "Health check failed"
exit 1

