# Geoffrey — Arquitectura del Ecosistema

> Sistema personal de reemplazo de servicios de streaming (Netflix, Spotify, etc.)
> basado en Telegram + Jellyfin + Syncthing.

---

## Diagrama de Arquitectura

```mermaid
graph TB
    subgraph "📡 Ingesta"
        TG[Usuario Telegram]
        BOT[geoffrey_bot.py<br/>Telethon MTProto]
        API[FastAPI :8000<br/>SQLite + WebSocket]
        DASH[Dashboard Web<br/>Tailwind + WS]
    end

    subgraph "💾 Almacenamiento"
        V[downloads/Video/]
        M[downloads/Music/]
        S[downloads/Series/]
        MV[downloads/Movies/]
        ARC[/mnt/avivo archive]
    end

    subgraph "⚙️ Procesamiento"
        JFH[jellyfin_headless.py<br/>cada 6h]
        MW[migrate_watched.py<br/>diario 12am]
    end

    subgraph "📤 Distribución"
        JF[Jellyfin :8096]
        ST[Syncthing]
        SMB[SMB Share]
    end

    subgraph "📱 Clientes"
        AIMP_MOBILE[AIMP Móvil<br/>vía Syncthing]
        AIMP_PC[AIMP Remoto<br/>vía SMB]
        JF_CLIENT[Jellyfin Client<br/>Web / TV / Móvil]
    end

    %% Flujo principal
    TG -->|envía archivo| BOT
    BOT -->|MIME clasifica| V
    BOT -->|MIME clasifica| M
    BOT -->|POST /tasks| API
    API -->|sirve| DASH
    DASH -->|WS updates| API

    %% Video pipeline
    V -->|cada 6h| JFH
    JFH -->|rename & move| S
    JFH -->|fallback| MV
    S --> JF
    MV --> JF
    JF -->|watched items| MW
    MW -->|copia + elimina| ARC

    %% Música pipeline
    M --> ST
    M --> SMB
    M --> JF
    ST -->|sincroniza| AIMP_MOBILE
    SMB -->|lectura remota| AIMP_PC
    JF -->|streaming| JF_CLIENT
```

---

## Capas del Sistema

### 1. Ingesta (Telegram)

| Componente | Tecnología | Función |
|---|---|---|
| Bot | `Telethon` (MTProto) | Recibe archivos, clasifica por MIME, encola descargas |
| API | `FastAPI` + `SQLite` | Centraliza estado de descargas, evita FloodWait |
| Dashboard | Tailwind + WebSocket | Monitoreo en vivo de descargas |

### 2. Procesamiento

| Script | Frecuencia | Función |
|---|---|---|
| `jellyfin_headless.py` | Cada 6h | Escanea `Video/`, parsea episodios, renombra y mueve a `Series/` o `Movies/` |
| `migrate_watched.py` | Diario 12 AM | Consulta Jellyfin items reproducidos, copia a `/mnt/avivo`, elimina original |

### 3. Distribución

| Servicio | Acceso | Propósito |
|---|---|---|
| **Jellyfin** (`:8096`) | Web, TV, móvil | Catálogo de series, películas y música |
| **Syncthing** | Red local | Sincroniza música al móvil |
| **SMB** | Red local | Lectura remota de MP3s desde AIMP en PC |

### 4. Clientes

| Dispositivo | App | Fuente |
|---|---|---|
| Móvil | AIMP | Syncthing (offline) |
| PC remoto | AIMP | SMB (streaming local) |
| Cualquiera | Jellyfin Web / Finamp / Gelli | Jellyfin API |

---

## Stack Tecnológico

- **Lenguaje:** Python 3.11+
- **Runtime:** Docker / docker-compose
- **Bot:** Telethon (Telegram MTProto)
- **API:** FastAPI + SQLModel + SQLite
- **Media Server:** Jellyfin
- **Sincronización:** Syncthing
- **Red:** SMB/CIFS
- **Dash:** Tailwind CSS + WebSocket

---

## Flujo de Datos

```
Usuario envía archivo → Telegram
         ↓
geoffrey_bot.py recibe vía MTProto
         ↓
Clasifica: Video → downloads/Video/
           Música → downloads/Music/
           Documento → downloads/Documents/
         ↓
Registra tarea en API (PENDING) → SQLite
         ↓
download_worker descarga con progreso (PATCH cada 3s)
         ↓
COMPLETED → WebSocket broadcast al dashboard
```

## Música: Distribución sin Streaming Central

La música no requiere un servidor de streaming dedicado:

1. **Syncthing** replica `downloads/Music/` al móvil → AIMP reproduce local
2. **SMB** exporta la misma carpeta → AIMP remoto lee directo del servidor
3. **Jellyfin** también indexa la carpeta como biblioteca musical (fallback)

