import os
import sys
import psycopg2
import requests
import sqlalchemy
from typing import List
from sqlalchemy import text
from .db import get_engine

# Required envs for all runs
REQUIRED_ENV_VARS = [
    "SECRET_KEY",
    "SUPABASE_URL",
    # Optional: SUPABASE_SERVICE_KEY for server-side checks. Anon key is typically client-only.
    # Keep SUPABASE_ANON_KEY optional unless your server specifically needs it.
]

def validate_env_vars(required: List[str] = None):
    required = required or REQUIRED_ENV_VARS
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")
    return True

def check_database_connection():
    if os.getenv("ENABLE_DB_CHECK", "false").lower() != "true":
        print("Database check skipped")
        return True

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is required when ENABLE_DB_CHECK=true")

    try:
        conn = psycopg2.connect(db_url, connect_timeout=5)
        conn.close()
        print("Database connection successful")
        return True
    except Exception as e:
        print("Database connection failed:", e)
        return False

def check_db_migrations():
    """
    Behavior:
      - If MIGRATION_REQUIRED_TABLES is set, check those tables exist.
      - Otherwise default to checking for 'alembic_version' (Alembic).
    """
    if os.getenv("ENABLE_MIGRATION_CHECK", "false").lower() != "true":
        print("Migration check skipped")
        return True

    engine = get_engine()
    tables_env = os.getenv("MIGRATION_REQUIRED_TABLES", "").strip()
    if tables_env:
        required_tables = [t.strip() for t in tables_env.split(",") if t.strip()]
    else:
        required_tables = ["alembic_version"]

    try:
        with engine.connect() as conn:
            for table in required_tables:
                res = conn.execute(
                    text(
                        """
                        SELECT EXISTS (
                          SELECT 1
                          FROM information_schema.tables
                          WHERE table_name = :table
                        );
                        """
                    ),
                    {"table": table},
                )
                exists = res.scalar()
                if not exists:
                    raise RuntimeError(f"Missing migration: table '{table}' does not exist")
        print("Database migrations validated")
        return True
    except Exception as e:
        print("Migration validation failed:", e)
        return False

def check_supabase_connectivity():
    """
    Optional: run when SUPABASE_SERVICE_KEY is present (server-side checks).
    We make a simple REST call to the Supabase REST endpoint; requires service key
    or an API key that allows server-side calls.
    """
    url = os.getenv("SUPABASE_URL")
    svc_key = os.getenv("SUPABASE_SERVICE_KEY")  # prefer service key for server checks
    if not url or not svc_key:
        print("Supabase check skipped (no SUPABASE_SERVICE_KEY or SUPABASE_URL)")
        return True

    try:
        # Example: call a lightweight endpoint — the REST endpoint requires proper auth
        headers = {"apikey": svc_key, "Authorization": f"Bearer {svc_key}"}
        r = requests.get(f"{url}/rest/v1/?select=1", headers=headers, timeout=5)
        if r.status_code in (200, 204):
            print("Supabase connectivity check passed")
            return True
        else:
            print("Supabase connectivity check returned status:", r.status_code, r.text)
            return False
    except Exception as e:
        print("Supabase connectivity check failed:", e)
        return False

def check_supabase_auth_and_storage():
    url = os.getenv("SUPABASE_URL")
    svc_key = os.getenv("SUPABASE_SERVICE_KEY")

    if not url or not svc_key:
        print("Supabase auth/storage check skipped")
        return True

    headers = {
        "apikey": svc_key,
        "Authorization": f"Bearer {svc_key}",
        "Content-Type": "application/json"
    }

    try:
        # Auth check
        auth_resp = requests.get(f"{url}/auth/v1/settings", headers=headers, timeout=5)
        if auth_resp.status_code != 200:
            print("Supabase auth check failed")
            return False

        # Storage check
        storage_resp = requests.get(f"{url}/storage/v1/bucket", headers=headers, timeout=5)
        if storage_resp.status_code not in (200, 204):
            print("Supabase storage check failed")
            return False

        print("Supabase auth & storage checks passed")
        return True
    except Exception as e:
        print("Supabase auth/storage check error:", e)
        return False


def run_startup_checks_and_exit_on_failure():
    # Env validation is strict by default; if you want to make SUPABASE optional remove it from REQUIRED_ENV_VARS
    try:
        validate_env_vars()
    except Exception as e:
        print("Env validation failed:", e)
        sys.exit(1)

    if not check_database_connection():
        sys.exit(1)

    if not check_db_migrations():
        sys.exit(1)

    # Optional: only run if SUPABASE_SERVICE_KEY present
    if not check_supabase_connectivity():
        sys.exit(1)

    if not check_supabase_auth_and_storage():
        sys.exit(1)

    print("Startup checks completed successfully")