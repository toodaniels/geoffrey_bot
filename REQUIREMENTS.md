# Geoffrey Download Dashboard — Technical Requirements

> Based on the design in `api/code.html`. Ordered by **ease of development** (from most immediate to most complex).

---

## Legend

| Symbol | Meaning |
|---------|-------------|
| ✅ | Already exists in the backend or frontend |
| 🟢 | Easy to implement (hours) |
| 🟡 | Moderate (1-2 days) |
| 🔴 | Complex (weeks or depends on new infrastructure) |

---

## 1. Replace the Current Dashboard with the New Design

| Item | Status | Requirements |
|------|--------|------------|
| Serve `code.html` as the main dashboard | 🟢 | Replace `templates/index.html` with `code.html` (the design is ready). Adjust asset paths (Tailwind CDN, Google Fonts) |
| WebSocket connection for live updates | ✅ | `api/websocket_manager.py` + `/ws` endpoint already exist. Only the JS integration in `code.html` is missing |
| Render active tasks from `GET /tasks/active` | ✅ | Endpoint already exists. The frontend connection is missing |

**Checklist:**
- [x] Backend: `GET /tasks/active`, `PATCH /tasks/{task_id}`, `/ws`
- [ ] Replace `templates/index.html` with the new design
- [ ] JS: connect the WebSocket and map `data.task → HTML card`
- [ ] JS: handle empty, error and reconnection states

---

## 2. File Type Icons on Cards

| Item | Status | Requirements |
|------|--------|------------|
| Show a Video/Music/Document icon based on `file_name` | 🟢 | The bot already detects the MIME type and stores it in `file_type`. Frontend: map extension → Material Symbol icon |

**Checklist:**
- [x] Bot: `get_file_type()` and `check_filename_type()` already exist
- [ ] Frontend: add the column/logic to show an icon based on file_name/ext
- [ ] Optional: add a `file_type` field to the API model so it can be served directly

---

## 3. Status Badges and Progress Bars

| Item | Status | Requirements |
|------|--------|------------|
| DOWNLOADING/PENDING/COMPLETED badge | 🟢 | The CSS is already in `code.html`. Only applying the class based on `task.status` is missing |
| Progress bar with shimmer animation | 🟢 | The `progress-shimmer` CSS already exists |
| Percentage and bytes downloaded | ✅ | `task.progress`, `task.downloaded_bytes`, `task.file_size_bytes` are already in the API |

**Checklist:**
- [x] The API returns `progress`, `downloaded_bytes`, `file_size_bytes`, `status`
- [ ] Frontend: map `task.status` to a CSS class (DOWNLOADING → green, PENDING → gray, COMPLETED → gold)
- [ ] Frontend: format bytes (B/KB/MB/GB) and percentage

---

## 4. Sidebar Filters: Videos / Music / Completed

| Item | Status | Requirements |
|------|--------|------------|
| `GET /tasks?type=video` endpoint | 🟢 | Add a `type` query param to the existing endpoint or create a new one. Filter by extension in the DB |
| `GET /tasks?status=completed` endpoint | 🟢 | Add a `status` query param to the existing endpoint. The DB already has a `status` field |
| Frontend connection on sidebar click | 🟢 | JS: change the endpoint based on the active tab, re-render the list |

**Checklist:**
- [x] The DB has `status` (PENDING, DOWNLOADING, COMPLETED, FAILED, CANCELLED)
- [ ] Backend: add `type` and `status` query params to `GET /tasks/active` or create `GET /tasks`
- [ ] Frontend: handle sidebar tabs with endpoint switching
- [ ] Frontend: active tab state with highlighted styling (already in `code.html`)

---

## 5. Real-Time Download Speed

| Item | Status | Requirements |
|------|--------|------------|
| Calculate MB/s from `report_progress` | 🟡 | The bot already has a callback every 3s. Compute the delta of bytes / delta of time |
| Store the speed in the API | 🟡 | Add an optional `download_speed` field to the `DownloadTask` model and the `DownloadTaskUpdate` schema |
| Display it in the frontend (e.g. "2.4 MB/s") | 🟢 | Only show the field when `status == DOWNLOADING` |

**Checklist:**
- [x] Bot: `report_progress()` runs every 3s with `received` and `total`
- [ ] Bot: compute `speed = (received - last_received) / (now - last_time)`
- [ ] API: add `download_speed: Optional[float]` to `DownloadTask` and `DownloadTaskUpdate`
- [ ] Frontend: show the speed when `status == DOWNLOADING`

---

## 6. Storage Status

| Item | Status | Requirements |
|------|--------|------------|
| `GET /storage/status` endpoint | 🟢 | Use `shutil.disk_usage(DOWNLOAD_PATH)` → total, used, free |
| Show free GB in a bento card | 🟢 | Frontend: render `free` in the "Storage Status" card |
| "Manage Storage" button | 🟡 | Could redirect to an endpoint that runs `migrate_watched.py` or show a management page |

**Checklist:**
- [x] Existing scripts: `migrate_watched.py`, `check_watched.py`
- [ ] Backend: `GET /storage` endpoint
- [ ] Frontend: connect the bento card to the endpoint data
- [ ] Optional: backend `POST /storage/cleanup` endpoint that runs the migration

---

## 7. Library Search

| Item | Status | Requirements |
|------|--------|------------|
| `GET /tasks?q=<query>` endpoint | 🟢 | SQL `WHERE file_name LIKE '%query%'` |
| Search input in the TopAppBar | 🟢 | The HTML already exists in `code.html`. JS: debounce + fetch + re-render |

**Checklist:**
- [ ] Backend: add a `q` query param to the listing endpoint
- [ ] Frontend: connect the search input with a debounce (300ms) to the endpoint

---

## 8. Resume All / Pause All

| Item | Status | Requirements |
|------|--------|------------|
| `POST /tasks/batch/update` endpoint | 🟡 | Accept a list of task_ids + a new status. SQL transaction |
| Resume All button → PENDING | 🟡 | Only for PAUSED tasks (a new status to consider) or FAILED |
| Pause All button → PAUSED | 🟡 | Requires a new `PAUSED` status in the enum, or cancelling active tasks |

> Note: the `PAUSED` status does not currently exist. We would need to decide whether to introduce it or whether "Pause All" cancels and "Resume All" retries.

**Checklist:**
- [ ] Decide: a new `PAUSED` status or reuse `CANCELLED`/`PENDING`?
- [ ] Backend: batch update endpoint
- [ ] Bot: handle paused tasks (do not take them from the queue)

---

## 9. Bento Stats: Total Bandwidth

| Item | Status | Requirements |
|------|--------|------------|
| Calculate total bandwidth (GB/day) | 🟡 | Sum `downloaded_bytes` of tasks COMPLETED today, divide by the hours of the day |
| `GET /stats/bandwidth` endpoint | 🟡 | Aggregated SQL query |
| Frontend: show it in a bento card | 🟢 | Render the value + usage bar |

**Checklist:**
- [x] The DB has `downloaded_bytes` and `updated_at`
- [ ] Backend: aggregated statistics endpoint
- [ ] Frontend: render the "Total Bandwidth" bento card

---

## 10. Play / Folder — Open File

| Item | Status | Requirements |
|------|--------|------------|
| `GET /files/{task_id}/download` endpoint | 🟡 | Serve a static file from `DOWNLOAD_PATH`. Direct stream |
| Play button → open the player | 🟡 | Frontend: `window.open()` or in-browser playback |
| Folder button → open the location | 🔴 | Not possible from the web. Alternative: copy the path to the clipboard or serve a ZIP |

**Checklist:**
- [ ] Backend: download/serve endpoint for a completed file
- [ ] Frontend: "Play" button opens the file in a new tab
- [ ] Frontend: "Folder" button copies the path to the clipboard

---

## 11. Add URL (Download by URL)

| Item | Status | Requirements |
|------|--------|------------|
| URL input + "Add URL" button in the sidebar | 🟢 | The HTML already exists. Modal or inline input |
| Backend `POST /download/url` | 🔴 | Receive a URL, validate it, queue the download |
| Integration with yt-dlp / aria2 | 🔴 | New worker in the bot for HTTP/S downloads |
| WebSocket progress broadcast | 🟡 | Reuse the existing `ConnectionManager.broadcast()` |

**Checklist:**
- [ ] Add `yt-dlp` or another lib to `pyproject.toml`
- [ ] Backend: `POST /tasks/url` endpoint that creates the task
- [ ] Bot: new URL download worker
- [ ] Frontend: "Add URL" modal/button + feedback

---

## 12. Settings Page

| Item | Status | Requirements |
|------|--------|------------|
| Route/serve the Settings page | 🟡 | New `/settings` route in FastAPI |
| Configuration form (ALLOWED_USERS, DOWNLOAD_PATH, etc.) | 🔴 | Requires config persistence in the DB or a file, and restarting services |
| "Manage Storage" button | 🟡 | Link to the cleanup/migrate action |

**Checklist:**
- [ ] Backend: config API endpoint
- [ ] Backend: settings persistence
- [ ] Frontend: form + saving

---

## 13. Authentication

| Item | Status | Requirements |
|------|--------|------------|
| Auth middleware in the API | 🔴 | All endpoints are currently public. Add JWT or an API Key |
| Login page | 🔴 | New route + form + token storage |
| Protect the WebSocket | 🔴 | Validate the token on the WS connection |

> ⚠️ The API currently has no authentication of any kind. If it is exposed publicly, this is critical.

**Checklist:**
- [ ] Decide on the scheme (API Key in a header vs JWT)
- [ ] Backend: authentication middleware
- [ ] Frontend: login flow
- [ ] Frontend: attach the token to fetch/WS

---

## Priority Summary

| Priority | Features | Effort |
|-----------|----------|----------|
| **P0** (now) | 1. New dashboard, 2. Icons, 3. Badges/Progress | Hours |
| **P1** (next) | 4. Sidebar filters, 5. Speed, 6. Storage status, 7. Search | 1-2 days |
| **P2** (short term) | 8. Resume/Pause All, 9. Bandwidth stats, 10. Play/Folder | 2-3 days |
| **P3** (medium term) | 11. Add URL, 12. Settings | 1-2 weeks |
| **P4** (long term) | 13. Authentication | Variable |

---

*Document generated from the design in `api/code.html` and an analysis of the existing code.*
