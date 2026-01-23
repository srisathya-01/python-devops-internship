#!/usr/bin/env bash
set -e

BASE_URL=${BASE_URL:-http://localhost:5000}

echo "Running smoke tests against $BASE_URL"

echo "Checking /health"
curl -fsS "$BASE_URL/health" | grep '"status": "ok"'

echo "✅ Smoke tests passed"



