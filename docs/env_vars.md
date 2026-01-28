# Environment variables

This file documents environment variables required to run the app.

Required
- SECRET_KEY — secret used by Flask for session signing (production: use a randomly generated secret)
- DATABASE_URL — SQLAlchemy DB URL, e.g. postgresql://user:pass@host:5432/dbname
- SUPABASE_URL — (if using Supabase) project URL
- SUPABASE_KEY — (if using Supabase) service role key for server-side operations

Optional
- PORT — server port (default 8080)

How to use
- Copy `.env.example` to `.env` and fill values for local testing.
- CI and production should set variables through the environment (secrets).