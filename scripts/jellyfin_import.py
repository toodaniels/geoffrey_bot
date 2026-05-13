import os
import re
import requests
from dotenv import load_dotenv

# Configuración básica
load_dotenv()
JELLYFIN_URL = os.getenv("JELLYFIN_URL")
JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY")
JELLYFIN_USER_ID = os.getenv("JELLYFIN_USER_ID")
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH")

def get_active_downloads():
    # Obtener logs del contenedor para identificar descargas activas
    log_stream = os.popen("podman logs geoffrey-bot | tail -n 100").read()
    pattern = r"Original filename: (.*?)\n"
    return re.findall(pattern, log_stream)

def find_series_id(series_name):
    if not JELLYFIN_API_KEY or not JELLYFIN_URL or not JELLYFIN_USER_ID:
        print("Error: Configuración de Jellyfin incompleta.")
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
    
    # Directorios soportados según geoffrey_bot.py
    supported_types = ['Video', 'Music', 'Documents']
    
    for type_folder in supported_types:
        folder_path = os.path.join(DOWNLOAD_PATH, type_folder)
        if not os.path.exists(folder_path):
            continue
            
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if not os.path.isfile(file_path):
                continue

            # Omitir si es un archivo en descarga
            if any(filename in active for active in active_downloads):
                print(f"Omitiendo {filename}: está en descarga activa.")
                continue
            
            # Lógica para identificar serie y episodio (solo para videos)
            if type_folder == 'Video':
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
