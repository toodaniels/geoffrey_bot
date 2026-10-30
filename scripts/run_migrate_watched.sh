#!/bin/bash
# Ejecuta el script de migración usando variables de entorno para evitar rutas absolutas hardcodeadas
cd "$(dirname "$0")/.."
source .env 2>/dev/null || true
poetry run python scripts/migrate_watched.py >> ../logs/migrate_watched.log 2>&1
