# Migrate Watched Media

This script automates the migration of media files marked as "watched" in Jellyfin from temporary download directories to the final storage disk (exFAT, `/mnt/media`).

## Requirements

- `python3`
- `requests`
- `python-dotenv`
- Access to the Jellyfin API (configured in `.env`)

## Configuration

Create a `.env` file in the root with the following variable:
`JELLYFIN_API_KEY=your_api_key_here`

Variables configured by default in the script:
- `USER_ID`: `your_jellyfin_user_id`
- `SOURCE_BASE_SERIES`: `/path/to/downloads/Series`
- `TARGET_BASE_SERIES`: `/mnt/media/Series`

## How It Works

1. Queries the Jellyfin API (`/Users/{USER_ID}/Items`) to get the list of items (`Movies`, `Episodes`) with the `IsPlayed` filter.
2. Translates the container's internal paths into local host paths.
3. Cleans the file names to comply with the `exFAT` filesystem restrictions (`clean_filename`).
4. Runs the migration:
   - Creates the necessary directories at the destination.
   - Copies the file using `shutil.copy2`.
   - Deletes the original file once verified.

## Running

The script is configured to run in real mode (no dry-run).

```bash
python migrate_watched.py
```
*Note: Make sure you have read permissions on the source and write permissions on the `/mnt/media` destination.*
