import os
import requests
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

API_KEY = os.getenv("JELLYFIN_API_KEY")
# Assuming the jellyfin host is reachable at http://myjellyfin:8096 or localhost:8096
# Since we are running inside or beside the container, localhost is usually fine
JELLYFIN_URL = "http://localhost:8096"
USER_ID = os.getenv("JELLYFIN_USER_ID")

headers = {
    "X-Emby-Token": API_KEY,
    "Content-Type": "application/json"
}

def get_watched_items():
    # Fetch items for the user with Played = True
    url = f"{JELLYFIN_URL}/Users/{USER_ID}/Items"
    params = {
        "Filters": "IsPlayed",
        "Recursive": "true",
        "IncludeItemTypes": "Movie,Episode",
        "Fields": "Path"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        items = response.json().get("Items", [])
        return items
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    watched = get_watched_items()
    if isinstance(watched, list):
        print(f"Found {len(watched)} watched items:")
        for item in watched[:10]: # Print first 10
            print(f"- {item.get('Name')} ({item.get('Type')}): {item.get('Path')}")
        if len(watched) > 10:
            print("...")
