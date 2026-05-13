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

## Automated Maintenance

- **Disk Cleanup:** A script `scripts/run_migrate_watched.sh` is scheduled to run daily at 12 AM via cron to perform disk space cleanup using `migrate_watched.py`.
- **Media Organization:** A script `scripts/jellyfin_headless.py` is scheduled to run every 6 hours via cron to automatically rename, classify, and organize media files into Jellyfin folders (Series/Movies), skipping active downloads detected from `geoffrey-bot` logs.

# Role & Workflow Protocol

## Git & PR Automation
You are an expert developer assistant. Whenever the user requests a code change, you must adhere to the following mandatory workflow:

1. **Branching:** Always create and switch to a new branch:
   `git checkout -b <descriptive-name>`

2. **Commit:** Stage and commit your changes:
   `git add .`
   `git commit -m "<descriptive-message>"`

3. **Pull Request:** Create the PR using GitHub CLI (gh):
   `gh pr create --title "<PR Title>" --body "<PR Description>\n\n--- \n*PR created automatically by the agent.*"`

## Guidelines
- Do not skip the branch creation step.
- Ensure the commit message is professional and concise.
- Always include the specific signature at the end of the PR body.
- If `gh` fails, stop and report the error to the user before attempting any further automated actions.

## PR Creation Workflow

When the user requests to create a branch, commit, and PR:
1. Always ask the user to confirm the plan before executing
2. Split related file changes logically (e.g., docker-compose with .gitignore, pyproject.toml with poetry.lock)
3. Create separate commit for AGENTS.md if it's new
4. Push the branch to remote
5. Create PR using `gh pr create` with the format:
   - Title: descriptive
   - Body: summary bullet points + "\n---\n*PR created automatically by Geoffrey.*"
6. Handle any merge conflicts with main before pushing the resolved changes
