import os
import re
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "./downloads/Video")

def get_active_downloads():
    """Obtiene los archivos actualmente en descarga desde los logs del bot."""
    log_stream = os.popen("podman logs geoffrey-bot | tail -n 100").read()
    pattern = r"Original filename: (.*?)\n"
    return re.findall(pattern, log_stream)

def process_file_with_tvnamer(file_path):
    """
    Ejecuta tvnamer en modo batch para renombrar automáticamente.
    -b: batch (renombrar sin intervención)
    -f: selectfirst (selecciona automáticamente el primer resultado de búsqueda)
    """
    try:
        print(f"Renombrando automáticamente: {file_path}")
        subprocess.run(
            ["poetry", "run", "tvnamer", "--batch", "--selectfirst", file_path],
            check=True, capture_output=True, text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al renombrar {file_path}: {e.stderr}")
        return False

def main():
    active_downloads = get_active_downloads()
    print(f"Descargas activas detectadas: {active_downloads}")
    
    # Procesar archivos en la carpeta de videos
    video_path = os.path.join(DOWNLOAD_PATH, "Video")
    if not os.path.exists(video_path):
        print(f"Carpeta no encontrada: {video_path}")
        return

    for filename in os.listdir(video_path):
        if filename.endswith(".mkv") or filename.endswith(".mp4"):
            # Omitir si es un archivo en descarga activa
            if any(filename in active for active in active_downloads):
                print(f"Omitiendo {filename}: está en descarga activa.")
                continue
            
            # Ejecutar tvnamer
            file_path = os.path.join(video_path, filename)
            process_file_with_tvnamer(file_path)

if __name__ == "__main__":
    main()
