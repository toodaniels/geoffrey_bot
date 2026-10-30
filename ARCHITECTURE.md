# Geoffrey — Ecosystem Architecture

> Personal streaming-service replacement (Netflix, Spotify, etc.)
> built on Telegram + Jellyfin + Syncthing.

---

## Architecture Diagram

```mermaid
graph TB
    subgraph "📡 Ingest"
        TG[Telegram User]
        BOT[geoffrey_bot.py<br/>Telethon MTProto]
        API[FastAPI :8000<br/>SQLite + WebSocket]
        DASH[Web Dashboard<br/>Tailwind + WS]
    end

    subgraph "💾 Storage"
        V[downloads/Video/]
        M[downloads/Music/]
        S[downloads/Series/]
        MV[downloads/Movies/]
        ARC[/mnt/media archive]
    end

    subgraph "⚙️ Processing"
        JFH[jellyfin_headless.py<br/>every 6h]
        MW[migrate_watched.py<br/>daily at 12am]
    end

    subgraph "📤 Distribution"
        JF[Jellyfin :8096]
        ST[Syncthing]
        SMB[SMB Share]
    end

    subgraph "📱 Clients"
        AIMP_MOBILE[AIMP Mobile<br/>via Syncthing]
        AIMP_PC[AIMP Remote<br/>via SMB]
        JF_CLIENT[Jellyfin Client<br/>Web / TV / Mobile]
    end

    %% Main flow
    TG -->|sends file| BOT
    BOT -->|MIME classifies| V
    BOT -->|MIME classifies| M
    BOT -->|POST /tasks| API
    API -->|serves| DASH
    DASH -->|WS updates| API

    %% Video pipeline
    V -->|every 6h| JFH
    JFH -->|rename & move| S
    JFH -->|fallback| MV
    S --> JF
    MV --> JF
    JF -->|watched items| MW
    MW -->|copy + delete| ARC

    %% Music pipeline
    M --> ST
    M --> SMB
    M --> JF
    ST -->|syncs| AIMP_MOBILE
    SMB -->|remote read| AIMP_PC
    JF -->|streaming| JF_CLIENT
```

---

## System Layers

### 1. Ingest (Telegram)

| Component | Technology | Role |
|---|---|---|
| Bot | `Telethon` (MTProto) | Receives files, classifies by MIME, queues downloads |
| API | `FastAPI` + `SQLite` | Centralizes download state, avoids FloodWait |
| Dashboard | Tailwind + WebSocket | Live download monitoring |

### 2. Processing

| Script | Frequency | Role |
|---|---|---|
| `jellyfin_headless.py` | Every 6h | Scans `Video/`, parses episodes, renames and moves them to `Series/` or `Movies/` |
| `migrate_watched.py` | Daily at 12 AM | Queries played items from Jellyfin, copies them to `/mnt/media`, deletes the original |

### 3. Distribution

| Service | Access | Purpose |
|---|---|---|
| **Jellyfin** (`:8096`) | Web, TV, mobile | Catalog of series, movies and music |
| **Syncthing** | Local network | Syncs music to the phone |
| **SMB** | Local network | Remote reading of MP3s from AIMP on PC |

### 4. Clients

| Device | App | Source |
|---|---|---|
| Mobile | AIMP | Syncthing (offline) |
| Remote PC | AIMP | SMB (local streaming) |
| Any | Jellyfin Web / Finamp / Gelli | Jellyfin API |

---

## Technology Stack

- **Language:** Python 3.11+
- **Runtime:** Docker / docker-compose
- **Bot:** Telethon (Telegram MTProto)
- **API:** FastAPI + SQLModel + SQLite
- **Media Server:** Jellyfin
- **Sync:** Syncthing
- **Network:** SMB/CIFS
- **Dashboard:** Tailwind CSS + WebSocket

---

## Data Flow

```
User sends file → Telegram
         ↓
geoffrey_bot.py receives it via MTProto
         ↓
Classifies: Video → downloads/Video/
            Music → downloads/Music/
            Document → downloads/Documents/
         ↓
Registers task in API (PENDING) → SQLite
         ↓
download_worker downloads with progress (PATCH every 3s)
         ↓
COMPLETED → WebSocket broadcast to the dashboard
```

## Music: Distribution Without Central Streaming

Music does not require a dedicated streaming server:

1. **Syncthing** replicates `downloads/Music/` to the phone → AIMP plays it locally
2. **SMB** exports the same folder → remote AIMP reads directly from the server
3. **Jellyfin** also indexes the folder as a music library (fallback)
