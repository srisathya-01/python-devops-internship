#!/usr/bin/env bash
set -euo pipefail

REQ_VARS=(
  DEPLOY_USER
  DEPLOY_HOST
  APP_DIR
  SSH_PRIVATE_KEY
  DATABASE_URL
)

missing=()
for v in "${REQ_VARS[@]}"; do
  if [ -z "${!v:-}" ]; then
    missing+=("$v")
  fi
done

if [ ${#missing[@]} -ne 0 ]; then
  echo "ERROR: Missing required environment variables: ${missing[*]}" >&2
  exit 1
fi

echo "All required environment variables set."
