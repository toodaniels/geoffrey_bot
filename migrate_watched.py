import os
import shutil
import requests
import re
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

API_KEY = os.getenv("JELLYFIN_API_KEY")
JELLYFIN_URL = "http://localhost:8096"
USER_ID = os.getenv("JELLYFIN_USER_ID", "4ae86364dc094a09b6b1aa0f655d6f2e")
SOURCE_BASE_SERIES = os.getenv("SOURCE_BASE_SERIES", "/home/toodaniels/Documents/geoffrey_telegram/downloads/Series")
SOURCE_BASE_MOVIES = os.getenv("SOURCE_BASE_MOVIES", "/home/toodaniels/Documents/geoffrey_telegram/downloads/Movies")
TARGET_BASE_SERIES = "/mnt/avivo/Series"
TARGET_BASE_MOVIES = "/mnt/avivo/Movies"

def clean_filename(filename):
    # Remove characters incompatible with exFAT/Windows
    return re.sub(r'[\\/*?:"<>|]', "", filename)

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
            
        source_path = translate_path(source_path)
        is_movie = item.get("Type") == "Movie"
        
        source_base = SOURCE_BASE_MOVIES if is_movie else SOURCE_BASE_SERIES
        target_base = TARGET_BASE_MOVIES if is_movie else TARGET_BASE_SERIES
        
        if not source_path.startswith(source_base):
            continue
        
        relative_path = os.path.relpath(source_path, source_base)
        
        # Clean path parts to avoid filesystem errors
        parts = relative_path.split(os.sep)
        clean_parts = [clean_filename(p) for p in parts]
        dest_path = os.path.join(target_base, *clean_parts)
        
        print(f"{'[DRY RUN] ' if dry_run else ''}Migrating {item.get('Type')}: {source_path} -> {dest_path}")
        
        if not dry_run:
            if os.path.exists(source_path):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                # Use copy2 then remove to handle cross-device moves
                shutil.copy2(source_path, dest_path)
                os.remove(source_path)
            else:
                print(f"File not found: {source_path}")

if __name__ == "__main__":
    migrate_items(dry_run=False)
