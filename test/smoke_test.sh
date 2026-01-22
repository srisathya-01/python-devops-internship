#!/usr/bin/env bash
set -e

BASE_URL=${BASE_URL:-http://localhost:5000}

echo "Running smoke tests against $BASE_URL"

echo "Checking /health"
curl -fsS "$BASE_URL/health" | grep '"ok":true'

echo "Checking /metrics"
curl -fsS "$BASE_URL/metrics" > /dev/null

echo "✅ Smoke tests passed"

#!/usr/bin/env bash
set -e

BASE_URL=${BASE_URL:-http://localhost:5000}

curl -f "$BASE_URL/health"
