# Migrate Watched Media

Este script automatiza la migración de archivos multimedia marcados como "vistos" en Jellyfin desde directorios de descarga temporales hacia el disco de almacenamiento final (exFAT, `/mnt/avivo`).

## Requisitos

- `python3`
- `requests`
- `python-dotenv`
- Acceso a Jellyfin API (configurado en `.env`)

## Configuración

Crea un archivo `.env` en la raíz con la siguiente variable:
`JELLYFIN_API_KEY=tu_api_key_aqui`

Variables configuradas por defecto en el script:
- `USER_ID`: 4ae86364dc094a09b6b1aa0f655d6f2e
- `SOURCE_BASE_SERIES`: `/home/toodaniels/Documents/geoffrey_telegram/downloads/Series`
- `TARGET_BASE_SERIES`: `/mnt/avivo/Series`

## Funcionamiento

1. Consulta Jellyfin API (`/Users/{USER_ID}/Items`) para obtener la lista de ítems (`Movies`, `Episodes`) con filtro `IsPlayed`.
2. Traduce las rutas internas de los contenedores a rutas locales del host.
3. Limpia los nombres de archivo para cumplir con las restricciones del sistema de archivos `exFAT` (`clean_filename`).
4. Ejecuta la migración:
   - Crea los directorios necesarios en el destino.
   - Copia el archivo mediante `shutil.copy2`.
   - Elimina el archivo original una vez verificado.

## Ejecución

El script está configurado para ejecutarse en modo real (sin dry-run).

```bash
python migrate_watched.py
```
*Nota: Asegúrate de tener permisos de lectura en la fuente y escritura en el destino `/mnt/avivo`.*
