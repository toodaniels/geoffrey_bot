import os
import requests
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()
JELLYFIN_URL = os.getenv("JELLYFIN_URL")
JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY")
JELLYFIN_USER_ID = os.getenv("JELLYFIN_USER_ID")

def get_series_list():
    if not JELLYFIN_API_KEY or not JELLYFIN_URL or not JELLYFIN_USER_ID:
        return ""
    headers = {"X-Emby-Token": JELLYFIN_API_KEY}
    url = f"{JELLYFIN_URL}/Items?userId={JELLYFIN_USER_ID}&IncludeItemTypes=Series&Recursive=true"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json().get("Items", [])
            return "\n".join([item["Name"] for item in items])
    except:
        pass
    return ""

def determine_series(filename):
    series_list = get_series_list()
    prompt = f"Tengo el archivo '{filename}'. Del siguiente listado de series en mi Jellyfin, determina a cuál pertenece. Contesta solo el nombre de la serie:\n\n{series_list}"
    
    # Llamada al agente (Hermes)
    try:
        result = subprocess.run(
            ["hermes", "chat", "-q", prompt],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(determine_series(sys.argv[1]))
    else:
        print("Uso: python scripts/jellyfin_headless.py <nombre_archivo>")
