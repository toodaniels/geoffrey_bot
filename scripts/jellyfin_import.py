import os
import re
import requests
from dotenv import load_dotenv

# Configuración básica
load_dotenv()
JELLYFIN_URL = os.getenv("JELLYFIN_URL", "http://myjellyfin:8096")
JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY")
JELLYFIN_USER_ID = "4ae86364dc094a09b6b1aa0f655d6f2e"
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "/home/toodaniels/Documents/geoffrey_telegram/downloads/Video")

def get_active_downloads():
    # Obtener logs del contenedor para identificar descargas activas
    log_stream = os.popen("podman logs geoffrey-bot | tail -n 100").read()
    pattern = r"Original filename: (.*?)\n"
    return re.findall(pattern, log_stream)

def find_series_id(series_name):
    if not JELLYFIN_API_KEY:
        print("Error: JELLYFIN_API_KEY no configurado.")
        return None
    headers = {"X-Emby-Token": JELLYFIN_API_KEY}
    # Búsqueda de la serie en Jellyfin
    url = f"{JELLYFIN_URL}/Items?userId={JELLYFIN_USER_ID}&searchTerm={series_name}&IncludeItemTypes=Series"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["Items"]:
                return data["Items"][0]["Id"]
    except Exception as e:
        print(f"Error conectando a Jellyfin: {e}")
    return None

def process_files(dry_run=True):
    active_downloads = get_active_downloads()
    print(f"Descargas activas detectadas en logs: {active_downloads}")
    
    for filename in os.listdir(DOWNLOAD_PATH):
        if filename.endswith(".mkv"):
            # Omitir si es un archivo en descarga
            if any(filename in active for active in active_downloads):
                print(f"Omitiendo {filename}: está en descarga activa.")
                continue
            
            # Ejemplo: "True Beauty - S0E7.mkv" -> Serie: "True Beauty"
            match = re.match(r"(.*?) - S\d+E\d+", filename)
            if match:
                series_name = match.group(1)
                series_id = find_series_id(series_name)
                if series_id:
                    print(f"Serie '{series_name}' identificada (ID: {series_id}).")
                    if dry_run:
                        print(f"[DRY-RUN] Procesando {filename} para Jellyfin.")
                    else:
                        print(f"Importando {filename} a la serie...")
                else:
                    print(f"No se pudo encontrar la serie '{series_name}' en Jellyfin.")

if __name__ == "__main__":
    process_files(dry_run=True)
