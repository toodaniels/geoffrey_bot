# Geoffrey Bot [![Docker Image Version (latest by date)](https://img.shields.io/docker/v/toodaniels/geoffrey_bot?label=ghcr.io/toodaniels/geoffrey_bot&sort=date)](https://github.com/toodaniels/geoffrey_bot/pkgs/container/geoffrey_bot)

A Telegram bot for downloading and managing media files.

## Features

- 📥 Download media files (videos, music, documents)
- 📂 List downloaded files by type
- 🚦 Queue system for multiple downloads
- 📊 Download progress bar with speed indicator
- 🔒 User access control via Telegram ID

## Requirements

- Python 3.7 or higher
- Telegram Developer Account
- Telegram Bot Token

## Installation

1. Clone the repository:
   ```bash
   git clone [REPOSITORY_URL]
   cd geoffrey_telegram
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🐳 Docker Usage

You can run Geoffrey Bot using the pre-built Docker image from GitHub Container Registry:

```bash
docker run -d \
  --name geoffrey-bot \
  -e API_ID=your_api_id \
  -e API_HASH=your_api_hash \
  -e TELEGRAM_BOT_TOKEN=your_bot_token \
  -e ALLOWED_USERS=your_telegram_id \
  -v /path/to/downloads:/app/downloads \
  ghcr.io/toodaniels/geoffrey_bot:main
```

### Environment Variables

- `API_ID`: Your Telegram API ID
- `API_HASH`: Your Telegram API hash
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `ALLOWED_USERS`: Comma-separated list of Telegram user IDs that are allowed to use the bot
- `DOWNLOAD_PATH`: (Optional) Path to store downloaded files (default: `/app/downloads`)

### Volumes

- `/app/downloads`: Directory where downloaded files will be stored

## Configuration

1. Create a `.env` file in the root directory with the following variables:
   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   TELEGRAM_BOT_TOKEN=your_bot_token
   ALLOWED_USERS=your_telegram_id,another_id
   DOWNLOAD_PATH=/path/to/downloads
   ```

2. To get your Telegram user ID, you can use [@userinfobot](https://t.me/userinfobot)

## Usage

### Available Commands

- `/start` or `/help` - Show help menu
- `/list video` or `/l video` - List video files
- `/list music` or `/l music` - List music files
- `/list document` or `/l document` - List documents

### How to Use

1. Start the bot:
   ```bash
   python geoffrey_bot.py
   ```

2. Send any media file to the bot to download it.

3. Use commands to list downloaded files.

## File Structure

```
geoffrey_telegram/
├── geoffrey_bot.py    # Main bot code
├── requirements.txt   # Dependencies
├── .env.example      # Example configuration
└── downloads/        # Download directory (auto-created)
    ├── Video/        # Downloaded videos
    ├── Music/        # Music files
    └── Documents/    # Documents
```

## Centralized Download API (New)

A centralized REST API (`api/`) was introduced to decouple download progress reporting from Telegram, eliminating `FloodWait` and rate-limiting issues.

### Stack

- **FastAPI** + **SQLModel** (SQLAlchemy + Pydantic)
- **SQLite** database (`geoffrey.db`)
- Interactive documentation at `/docs` (Swagger UI) and `/redoc` (ReDoc)

### Running the API

```bash
poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Running the API with Docker Compose

The API has its own image (`api/Dockerfile`, based on `python:3.11-slim`) and is defined as the `geoffrey-api` service in the general `docker-compose.yml`. It exposes port `8000` and bind-mounts `geoffrey.db` so tasks survive container recreations.

```bash
docker compose build geoffrey-api
docker compose up -d geoffrey-api
# or run the whole stack
docker compose up -d
```

The container exposes a `/health` endpoint, used by the Compose healthcheck. The bot reaches the API through the host gateway (`API_BASE_URL` in `.env`), so it keeps working without being recreated.

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health probe used by Docker/Compose |
| `POST` | `/tasks` | Register a new download task |
| `PATCH` | `/tasks/{task_id}` | Update a task's progress/status |

### State Flow Diagram

```
PENDING → DOWNLOADING → COMPLETED
                        → FAILED
                        → CANCELLED
```

### `POST /tasks`

Creates a task with status `PENDING`.

**Body:**
```json
{
  "user_id": 1448666148,
  "message_id": 12345,
  "file_name": "video.mp4",
  "file_size_bytes": 1048576
}
```

**Response (201):**
```json
{
  "task_id": "uuid-string",
  "status": "PENDING",
  "message": "Task registered successfully"
}
```

### `PATCH /tasks/{task_id}`

Updates a task partially (all fields are optional).

**Body:**
```json
{
  "status": "DOWNLOADING",
  "progress": 0.45,
  "downloaded_bytes": 471859
}
```

**Response (200):** Full `DownloadTask` object.

### `DownloadTask` Model

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | UUID (PK) | Unique identifier |
| `user_id` | int | Telegram user ID |
| `message_id` | int | Telegram message ID |
| `file_name` | string | File name |
| `file_size_bytes` | int? | Size in bytes |
| `status` | enum | `PENDING` / `DOWNLOADING` / `COMPLETED` / `FAILED` / `CANCELLED` |
| `progress` | float (0.0-1.0) | Download progress |
| `downloaded_bytes` | int | Bytes downloaded |
| `error_message` | string? | Error message if it failed |
| `created_at` | datetime | Creation date |
| `updated_at` | datetime | Last update date |

### Tests

```bash
poetry run python -m unittest api.test_main
```

### Running in Development

To run both services locally, you need two terminals:

**Terminal 1 — API:**
```bash
poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
The `--reload` flag restarts the server automatically when it detects code changes.

**Terminal 2 — Bot:**
```bash
DEVELOPMENT=1 poetry run python geoffrey_bot.py
```
The `DEVELOPMENT=1` variable makes the bot load the `.env` file automatically (see `AGENTS.md` for details).

The bot connects to the API at `http://localhost:8000` by default. Make sure the API is running before starting the bot.

---



## Recent Bot Changes

### Refactor: Decoupling progress reporting (`43f9ca2`)

The bot used to edit Telegram messages on every progress update, which caused `FloodWait` blocks. Now:

1. **Centralized registration:** When a download starts, the bot calls `POST /tasks` to register the task in the API and receives a `task_id`.
2. **Throttled reporting:** Progress is sent via `PATCH /tasks/{task_id}` every **3 seconds** at most, using `aiohttp` asynchronously.
3. **Final states:** On completion, it sends `COMPLETED` with `progress=1.0`; if it fails or the timeout expires (6h), it sends `FAILED`.
4. **Telegram messages:** They are now secondary (best-effort); if they fail due to `FloodWait`, they are logged without affecting the download.

### Added dependencies

- `aiohttp` — Async HTTP client for communicating with the API
- `fastapi` + `sqlmodel` + `uvicorn` — Server and ORM for the centralized API

### Environment variables

In addition to the existing ones, the API is configured at `http://localhost:8000` by default (the `API_BASE_URL` constant in `geoffrey_bot.py`). For production, it can be changed or read from an environment variable.

## Troubleshooting

If you encounter any issues:
1. Verify all environment variables are set correctly
2. Ensure you have write permissions in the download directory
3. Check the bot logs for error messages

## License

[MIT License](LICENSE)