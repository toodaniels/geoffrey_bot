import os
import shutil
import requests
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

API_KEY = os.getenv("JELLYFIN_API_KEY")
JELLYFIN_URL = "http://localhost:8096"
USER_ID = "4ae86364dc094a09b6b1aa0f655d6f2e" # Updated user ID
SOURCE_BASE_SERIES = "/home/toodaniels/Documents/geoffrey_telegram/downloads/Series"
SOURCE_BASE_MOVIES = "/home/toodaniels/Documents/geoffrey_telegram/downloads/Movies"
TARGET_BASE_SERIES = "/mnt/avivo/Series"
TARGET_BASE_MOVIES = "/mnt/avivo/Movies"

# Map Jellyfin's internal paths to host paths
def translate_path(path):
    if "/media/Series" in path:
        return path.replace("/media/Series", SOURCE_BASE_SERIES)
    if "/media/Movies" in path:
        return path.replace("/media/Movies", SOURCE_BASE_MOVIES)
    return path

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
            
        # Translate internal container path to host path
        source_path = translate_path(source_path)
            
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
            if os.path.exists(source_path):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.move(source_path, dest_path)
            else:
                print(f"File not found: {source_path}")

if __name__ == "__main__":
    migrate_items(dry_run=False)
