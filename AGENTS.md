# Geoffrey Telegram Bot

## Run

```bash
python geoffrey_bot.py
```

## Dev Mode

Set `DEVELOPMENT=1` to load `.env` file automatically.

## Env Required

- `API_ID`
- `API_HASH`
- `TELEGRAM_BOT_TOKEN`
- `ALLOWED_USERS` (comma-separated)
- `DOWNLOAD_PATH`

## Package Manager

Poetry (`poetry install`, `poetry run`).

## Docker Build

Push to `main` or create a `v*.*.*` tag triggers GitHub Actions to build and push to GHCR (`ghcr.io/toodaniels/geoffrey_telegram`).

## Tech Stack

- Python 3.10+ (from pyproject.toml)
- Telethon (Telegram client)
- python-telegram-bot (bot API)
- beets (music metadata)
- tvnamer (TV episode naming)