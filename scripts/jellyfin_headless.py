import os
import re
import subprocess
import shutil
import logging
from dotenv import load_dotenv

load_dotenv()
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "./downloads")
SERIES_BASE = os.getenv("SOURCE_BASE_SERIES", os.path.join(DOWNLOAD_PATH, "Series"))
MOVIES_BASE = os.getenv("SOURCE_BASE_MOVIES", os.path.join(DOWNLOAD_PATH, "Movies"))

logging.basicConfig(level=logging.INFO)

def get_active_downloads():
    log_stream = os.popen("podman logs geoffrey-bot | tail -n 100").read()
    pattern = r"Original filename: (.*?)\n"
    return re.findall(pattern, log_stream)

def organize_media(file_path):
    """
    Identifica si es serie o película y mueve a la carpeta correspondiente.
    Usa tvnamer para obtener metadatos y renombrar.
    """
    filename = os.path.basename(file_path)
    
    # 1. Renombrar usando tvnamer
    try:
        logging.info(f"Renombrando con tvnamer: {filename}")
        subprocess.run(["poetry", "run", "tvnamer", "--batch", "--selectfirst", "--move", file_path], 
                       check=True, capture_output=True, text=True)
        # El archivo ya debería estar renombrado. tvnamer suele mantenerlo en el directorio 
        # o moverlo si se configura. Por simplicidad, buscamos el archivo renombrado en la misma carpeta.
    except Exception as e:
        logging.error(f"Error con tvnamer: {e}")
        return

    # 2. Lógica de organización (Detectar serie o película)
    # Ejemplo de nombre de tvnamer: "True Beauty - S01E07.mkv"
    match = re.search(r"(.*) - S(\d+)E(\d+)", filename, re.IGNORECASE)
    
    if match:
        series_name, season, episode = match.groups()
        target_dir = os.path.join(SERIES_BASE, series_name.strip(), f"Season {int(season)}")
        os.makedirs(target_dir, exist_ok=True)
        shutil.move(file_path, os.path.join(target_dir, filename))
        logging.info(f"Movido a serie: {target_dir}")
    else:
        # Si no es serie, a Movies
        os.makedirs(MOVIES_BASE, exist_ok=True)
        shutil.move(file_path, os.path.join(MOVIES_BASE, filename))
        logging.info(f"Movido a películas: {MOVIES_BASE}")

def main():
    active_downloads = get_active_downloads()
    video_path = os.path.join(DOWNLOAD_PATH, "Video")
    
    if not os.path.exists(video_path):
        return

    # Procesar archivos en la carpeta de videos
    for root, dirs, files in os.walk(DOWNLOAD_PATH):
        for filename in files:
            if filename.endswith((".mkv", ".mp4")):
                # Omitir si es un archivo en descarga activa
                if any(filename in active for active in active_downloads):
                    print(f"Omitiendo {filename}: está en descarga activa.")
                    continue
                
                file_path = os.path.join(root, filename)
                organize_media(file_path)


if __name__ == "__main__":
    main()
