#!/bin/bash

set +e  # disable errexit (important for GitHub Actions)

BASE_URL="http://localhost:5000"

echo "Running smoke tests against $BASE_URL"
echo "Checking /health"

for i in {1..10}; do
  curl -fsS "$BASE_URL/health" > /dev/null
  if [ $? -eq 0 ]; then
    echo "Health check passed"
    exit 0
  fi
  echo "Waiting for app to be ready..."
  sleep 2
done

echo "Health check failed"
exit 1

