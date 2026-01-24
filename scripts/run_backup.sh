#!/usr/bin/env bash
set -e
mkdir -p backups
python scripts/backup_postgres.py backups/
