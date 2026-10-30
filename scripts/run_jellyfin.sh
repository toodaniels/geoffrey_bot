#!/bin/bash
# Run from the repository root so relative paths resolve correctly
cd "$(dirname "$0")/.."
poetry run python scripts/jellyfin_headless.py
