#!/usr/bin/env bash
set -e

REQUIRED_VARS=(
  DATABASE_URL
)

OPTIONAL_VARS=(
  SUPABASE_URL
  SUPABASE_KEY
)

echo "Validating required environment variables..."

missing=0
for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var}" ]; then
    echo "❌ Missing required variable: $var"
    missing=1
  else
    echo "✅ $var is set"
  fi
done

if [ "$missing" -eq 1 ]; then
  echo "Environment validation failed"
  exit 1
fi

echo "Environment validation passed"


