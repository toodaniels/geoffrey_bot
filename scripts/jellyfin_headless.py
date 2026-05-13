import os
import re
import requests
import argparse
from dotenv import load_dotenv

load_dotenv()
JELLYFIN_URL = os.getenv("JELLYFIN_URL")
JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY")
JELLYFIN_USER_ID = os.getenv("JELLYFIN_USER_ID")

def list_jellyfin_series():
    """Obtiene la lista de series disponibles en Jellyfin."""
    if not JELLYFIN_API_KEY or not JELLYFIN_URL or not JELLYFIN_USER_ID:
        return {}
    headers = {"X-Emby-Token": JELLYFIN_API_KEY}
    url = f"{JELLYFIN_URL}/Items?userId={JELLYFIN_USER_ID}&IncludeItemTypes=Series&Recursive=true"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return {item["Name"]: item["Id"] for item in response.json().get("Items", [])}
    except Exception as e:
        print(f"Error consultando series: {e}")
    return {}

def identify_series(filename, series_map):
    """Intenta identificar la serie por el nombre del archivo comparándolo con las series de Jellyfin."""
    # Intentar limpiar el nombre
    clean_name = re.sub(r' - S\d+E\d+.*', '', filename)
    clean_name = clean_name.replace('.', ' ').strip()
    
    # Búsqueda difusa simple
    for series_name in series_map:
        if clean_name.lower() in series_name.lower() or series_name.lower() in clean_name.lower():
            return series_name, series_map[series_name]
    return None, None

def main(filename):
    series_map = list_jellyfin_series()
    if not series_map:
        print("No se pudo conectar a Jellyfin o no hay series.")
        return

    name, sid = identify_series(filename, series_map)
    if name:
        print(f"MATCH|{name}|{sid}")
    else:
        print("NOMATCH")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Nombre del archivo a procesar")
    args = parser.parse_args()
    main(args.filename)
