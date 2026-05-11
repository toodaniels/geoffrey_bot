#!/bin/bash
cd /home/toodaniels/Documents/geoffrey_telegram
poetry run python migrate_watched.py >> /home/toodaniels/logs/migrate_watched.log 2>&1
