import os
import requests
from dotenv import load_dotenv

load_dotenv()
JELLYFIN_URL = os.getenv("JELLYFIN_URL")
JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY")
JELLYFIN_USER_ID = os.getenv("JELLYFIN_USER_ID")

def list_jellyfin_series():
    if not JELLYFIN_API_KEY or not JELLYFIN_URL or not JELLYFIN_USER_ID:
        print(f"Error: Configuración incompleta. URL={JELLYFIN_URL}, KEY={bool(JELLYFIN_API_KEY)}, USER={JELLYFIN_USER_ID}")
        return {}
    headers = {"X-Emby-Token": JELLYFIN_API_KEY}
    url = f"{JELLYFIN_URL}/Items?userId={JELLYFIN_USER_ID}&IncludeItemTypes=Series&Recursive=true"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json().get("Items", [])
            return {item["Name"]: item["Id"] for item in items}
        else:
            print(f"Error Jellyfin: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error consultando series: {e}")
    return {}

series = list_jellyfin_series()
for name in series:
    print(name)
