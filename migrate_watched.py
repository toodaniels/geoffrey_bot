import os
import shutil
import requests
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

API_KEY = os.getenv("JELLYFIN_API_KEY")
JELLYFIN_URL = "http://localhost:8096"
USER_ID = "4ae86364dc094a09b6b1aa0f655d6f2e" # Updated user ID
SOURCE_BASE_SERIES = "/media/Series"
SOURCE_BASE_MOVIES = "/media/Movies"
TARGET_BASE_SERIES = "/mnt/avivo/Series"
TARGET_BASE_MOVIES = "/mnt/avivo/Movies"

headers = {
    "X-Emby-Token": API_KEY,
    "Content-Type": "application/json"
}

def get_watched_items():
    url = f"{JELLYFIN_URL}/Users/{USER_ID}/Items"
    params = {
        "Filters": "IsPlayed",
        "Recursive": "true",
        "IncludeItemTypes": "Movie,Episode",
        "Fields": "Path"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json().get("Items", [])

def migrate_items(dry_run=True):
    watched = get_watched_items()
    for item in watched:
        source_path = item.get("Path")
        if not source_path:
            continue
            
        is_movie = item.get("Type") == "Movie"
        
        # Determine source and target base based on item type
        source_base = SOURCE_BASE_MOVIES if is_movie else SOURCE_BASE_SERIES
        target_base = TARGET_BASE_MOVIES if is_movie else TARGET_BASE_SERIES
        
        if not source_path.startswith(source_base):
            continue
        
        relative_path = os.path.relpath(source_path, source_base)
        dest_path = os.path.join(target_base, relative_path)
        
        print(f"{'[DRY RUN] ' if dry_run else ''}Moving {item.get('Type')}: {source_path} -> {dest_path}")
        
        if not dry_run:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.move(source_path, dest_path)

if __name__ == "__main__":
    migrate_items(dry_run=True)
