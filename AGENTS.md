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

You are an expert developer assistant. Whenever the user requests a code change, follow this workflow.

### 1. Sync `main`

Always branch from an up-to-date `main`:

```bash
git checkout main
git pull --ff-only
```

### 2. Create the branch

Never work directly on `main`. Use a short, descriptive `kebab-case` name with a type prefix:

| Prefix | Use for |
|---|---|
| `feat/<short-name>` | New features |
| `fix/<short-name>` | Bug fixes |
| `docs/<short-name>` | Documentation only |
| `refactor/<short-name>` | Restructuring without behavior change |
| `chore/<short-name>` | Maintenance, config, sanitation |
| `build/<short-name>` | Docker, CI or dependency changes |

```bash
git checkout -b feat/short-name
```

### 3. Commit

Group related changes into logical commits and stage files explicitly:

```bash
git add <path> <path>
git commit -m "feat(scope): short imperative summary"
```

- Follow Conventional Commits: `type(scope): summary` (e.g. `docs(arcane): ...`, `build(docker): ...`).
- Split unrelated changes into separate commits (e.g. compose file with `.dockerignore`, `pyproject.toml` with `poetry.lock`).
- Keep a separate commit when `AGENTS.md` is new.
- Prefer `git add <path>` over `git add .` so unrelated work is never included.

Before committing, confirm the diff contains only the intended files and no secrets.

### 4. Push

Publish the branch with upstream tracking:

```bash
git push -u origin <branch>
```

### 5. Create the PR

```bash
gh pr create --title "<descriptive title>" --body-file <body-file>
```

- Write the body to a scratch file and pass it with `--body-file`. This avoids shell quoting problems with multi-line Markdown and code blocks.
- Use `--base main` when the branch was not created from `main`.

## PR Body Structure

A PR must be descriptive. Write it in Markdown with these sections:

1. **Summary** — what the PR does and why.
2. **Changes** — bullets grouped by area (docs, config, scripts, etc.).
3. **Verification** — commands run and their result.
4. **Deployment notes** — required follow-up after merge (only when applicable).
5. **Signature** — always end the body with:

   ```
   ---
   *PR created automatically by the agent.*
   ```

After creating the PR, confirm it and report the URL:

```bash
gh pr view <number> --json number,title,state,url,headRefName,baseRefName
```

## Guidelines

- Do not skip the branch creation step.
- Keep commit messages and PR titles professional and concise.
- Always include the signature at the end of the PR body.
- If `gh` fails, stop and report the error to the user before attempting any further automated actions.
- Handle any merge conflicts with `main` before pushing the resolved changes.

## Sensitive Data

Never commit or document sensitive or environment-specific data:

- Tokens, API keys, session files or `.env` contents.
- Real host paths, LAN IPs, ports or usernames.
- Real Telegram or Jellyfin user IDs.

Use placeholders instead:

| Placeholder | Replaces |
|---|---|
| `/path/to/...` | Absolute host paths |
| `your_username` | Telegram handles |
| `your_jellyfin_user_id` | Jellyfin user IDs |
| `123456789` | Telegram user IDs |
| `192.168.1.100` | Private LAN IPs |
| `/mnt/media` | Private storage mounts |

Before staging, check for accidental leaks:

```bash
git grep -nE '/home/|/mnt/|192\.168\.' -- . ':!*.lock' ':!AGENTS.md'
```
