import os
import shutil
import requests
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

API_KEY = os.getenv("JELLYFIN_API_KEY")
JELLYFIN_URL = "http://localhost:8096"
USER_ID = "4ae86364dc094a09b6b1aa0f655d6f2e" # Updated user ID
TARGET_BASE = "/mnt/avivo/Series"
SOURCE_BASE = "/media/Series" # As seen in the Jellyfin API path

headers = {
    "X-Emby-Token": API_KEY,
    "Content-Type": "application/json"
}

def get_watched_items():
    url = f"{JELLYFIN_URL}/Users/{USER_ID}/Items"
    params = {
        "Filters": "IsPlayed",
        "Recursive": "true",
        "IncludeItemTypes": "Episode",
        "Fields": "Path"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json().get("Items", [])

def migrate_episodes(dry_run=True):
    watched = get_watched_items()
    for item in watched:
        source_path = item.get("Path")
        if not source_path or not source_path.startswith(SOURCE_BASE):
            continue
        
        # Calculate destination path: /media/Series/Serie/Season/File -> /mnt/avivo/Series/Serie/Season/File
        relative_path = os.path.relpath(source_path, SOURCE_BASE)
        dest_path = os.path.join(TARGET_BASE, relative_path)
        
        print(f"{'[DRY RUN] ' if dry_run else ''}Moving: {source_path} -> {dest_path}")
        
        if not dry_run:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.move(source_path, dest_path)

if __name__ == "__main__":
    # Start as dry-run by default
    migrate_episodes(dry_run=True)
