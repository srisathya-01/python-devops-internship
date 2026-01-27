#!/usr/bin/env sh
set -eu

echo "Running startup checks..."
python -c "from src.app.startup import run_startup_checks_and_exit_on_failure; run_startup_checks_and_exit_on_failure()"

# Wait for Postgres if DATABASE_URL is present by trying to connect a few times (simple loop)
if [ "${ENABLE_DB_CHECK:-false}" = "true" ] && [ -n "${DATABASE_URL:-}" ]; then
  echo "Waiting for database to become available..."
  # Try connecting via psycopg2 in a small python loop
  python - <<'PY'
import os, time, psycopg2, sys
db = os.getenv("DATABASE_URL")
for i in range(30):
    try:
        conn = psycopg2.connect(db, connect_timeout=2)
        conn.close()
        print("Database is ready")
        sys.exit(0)
    except Exception:
        time.sleep(1)
print("Timed out waiting for database")
sys.exit(1)
PY
fi

# Run alembic upgrade head only if enabled AND migrations folder exists
if [ "${ENABLE_MIGRATION_CHECK:-false}" = "true" ] && [ -d "./migrations" ]; then
  echo "Applying migrations with alembic..."
  alembic upgrade head
else
  echo "Skipping alembic upgrade (ENABLE_MIGRATION_CHECK not true or migrations/ not present)"
fi

echo "Starting backend..."
exec "$@"