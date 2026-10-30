# Geoffrey Download Dashboard — Technical Requirements

> Basado en el diseño de `api/code.html`. Ordenado por **posibilidad de desarrollo** (de más inmediato a más complejo).

---

## Leyenda

| Símbolo | Significado |
|---------|-------------|
| ✅ | Ya existe en backend o frontend |
| 🟢 | Fácil de implementar (horas) |
| 🟡 | Moderado (1-2 días) |
| 🔴 | Complejo (semanas o depende de nueva infraestructura) |

---

## 1. Reemplazar Dashboard Actual con el Nuevo Diseño

| Ítem | Estado | Requisitos |
|------|--------|------------|
| Servir `code.html` como dashboard principal | 🟢 | Reemplazar `templates/index.html` con `code.html` (el diseño ya está listo). Ajustar rutas de assets (Tailwind CDN, Google Fonts) |
| Conexión WebSocket para updates en vivo | ✅ | `api/websocket_manager.py` + endpoint `/ws` ya existen. Solo falta integrar JS en `code.html` |
| Renderizar tareas activas desde `GET /tasks/active` | ✅ | Endpoint ya existe. Falta conectar frontend |

**Checklist:**
- [x] Backend: `GET /tasks/active`, `PATCH /tasks/{task_id}`, `/ws`
- [ ] Reemplazar `templates/index.html` con el nuevo diseño
- [ ] JS: conectar WebSocket y mapear `data.task → tarjeta HTML`
- [ ] JS: manejar estados vacío, error, reconexión

---

## 2. Iconos de Tipo de Archivo en Tarjetas

| Ítem | Estado | Requisitos |
|------|--------|------------|
| Mostrar icono Video/Music/Document según `file_name` | 🟢 | El bot ya detecta tipo MIME y lo guarda en `file_type`. Frontend: mapear extensión → icono Material Symbol |

**Checklist:**
- [x] Bot: `get_file_type()` y `check_filename_type()` ya existen
- [ ] Frontend: agregar columna/lógica para mostrar icono según file_name/ext
- [ ] Opcional: agregar campo `file_type` al modelo API para servirlo directamente

---

## 3. Badges de Estado y Barras de Progreso

| Ítem | Estado | Requisitos |
|------|--------|------------|
| Badge DOWNLOADING/PENDING/COMPLETED | 🟢 | CSS ya está en `code.html`. Solo falta aplicar clase según `task.status` |
| Progress bar con animación shimmer | 🟢 | CSS con `progress-shimmer` ya existe |
| Porcentaje y bytes descargados | ✅ | `task.progress`, `task.downloaded_bytes`, `task.file_size_bytes` ya están en API |

**Checklist:**
- [x] API devuelve `progress`, `downloaded_bytes`, `file_size_bytes`, `status`
- [ ] Frontend: mapear `task.status` a clase CSS (DOWNLOADING → verde, PENDING → gris, COMPLETED → dorado)
- [ ] Frontend: formatear bytes (B/KB/MB/GB) y porcentaje

---

## 4. Filtros Sidebar: Videos / Music / Completed

| Ítem | Estado | Requisitos |
|------|--------|------------|
| Endpoint `GET /tasks?type=video` | 🟢 | Agregar query param `type` a endpoint existente o crear nuevo. Filtrar por extensión en DB |
| Endpoint `GET /tasks?status=completed` | 🟢 | Agregar query param `status` a endpoint existente. DB ya tiene campo `status` |
| Conexión frontend al hacer clic en sidebar | 🟢 | JS: cambiar endpoint según tab activo, re-renderizar lista |

**Checklist:**
- [x] DB tiene `status` (PENDING, DOWNLOADING, COMPLETED, FAILED, CANCELLED)
- [ ] Backend: agregar query params `type` y `status` a `GET /tasks/active` o crear `GET /tasks`
- [ ] Frontend: manejar tabs de sidebar con cambio de endpoint
- [ ] Frontend: active tab state con estilo destacado (ya existe en `code.html`)

---

## 5. Velocidad de Descarga en Tiempo Real

| Ítem | Estado | Requisitos |
|------|--------|------------|
| Calcular MB/s desde `report_progress` | 🟡 | El bot ya tiene callback cada 3s. Calcular delta de bytes / delta de tiempo |
| Almacenar velocidad en API | 🟡 | Agregar campo opcional `download_speed` al modelo `DownloadTask` y schema `DownloadTaskUpdate` |
| Mostrar en frontend (ej: "2.4 MB/s") | 🟢 | Solo mostrar campo si `status == DOWNLOADING` |

**Checklist:**
- [x] Bot: `report_progress()` se ejecuta cada 3s con `received` y `total`
- [ ] Bot: calcular `speed = (received - last_received) / (now - last_time)`
- [ ] API: agregar `download_speed: Optional[float]` a `DownloadTask` y a `DownloadTaskUpdate`
- [ ] Frontend: mostrar speed cuando `status == DOWNLOADING`

---

## 6. Estado de Almacenamiento (Storage Status)

| Ítem | Estado | Requisitos |
|------|--------|------------|
| Endpoint `GET /storage/status` | 🟢 | Usar `shutil.disk_usage(DOWNLOAD_PATH)` → total, used, free |
| Mostrar GB libres en bento card | 🟢 | Frontend: renderizar `free` en la card "Storage Status" |
| Botón "Manage Storage" | 🟡 | Podría redirigir a endpoint que ejecute `migrate_watched.py` o mostrar página de gestión |

**Checklist:**
- [x] Scripts existentes: `migrate_watched.py`, `check_watched.py`
- [ ] Backend: endpoint `GET /storage`
- [ ] Frontend: conectar bento card con data del endpoint
- [ ] Opcional: backend endpoint `POST /storage/cleanup` que ejecute migración

---

## 7. Búsqueda en Biblioteca

| Ítem | Estado | Requisitos |
|------|--------|------------|
| Endpoint `GET /tasks?q=<query>` | 🟢 | SQL `WHERE file_name LIKE '%query%'` |
| Input de búsqueda en TopAppBar | 🟢 | HTML ya existe en `code.html`. JS: debounce + fetch + re-render |

**Checklist:**
- [ ] Backend: agregar query param `q` a endpoint de listado
- [ ] Frontend: conectar search input con debounce (300ms) al endpoint

---

## 8. Resume All / Pause All

| Ítem | Estado | Requisitos |
|------|--------|------------|
| Endpoint `POST /tasks/batch/update` | 🟡 | Aceptar lista de task_ids + nuevo status. Transacción SQL |
| Botón Resume All → PENDING | 🟡 | Solo para tareas PAUSED (nuevo status a considerar) o FAILED |
| Botón Pause All → PAUSED | 🟡 | Requiere nuevo status `PAUSED` en enum, o cancelar tareas activas |

> Nota: el status `PAUSED` no existe actualmente. Habría que decidir si se introduce o si "Pause All" cancela y "Resume All" re-intenta.

**Checklist:**
- [ ] Decidir: ¿nuevo status `PAUSED` o reusar `CANCELLED`/`PENDING`?
- [ ] Backend: endpoint batch update
- [ ] Bot: manejar tareas pausadas (no tomarlas del queue)

---

## 9. Bento Stats: Total Bandwidth

| Ítem | Estado | Requisitos |
|------|--------|------------|
| Calcular ancho de banda total (GB/día) | 🟡 | Sumar `downloaded_bytes` de tareas COMPLETED hoy, dividir entre horas del día |
| Endpoint `GET /stats/bandwidth` | 🟡 | Query agregado SQL |
| Frontend: mostrar en bento card | 🟢 | Renderizar dato + barra de uso |

**Checklist:**
- [x] DB tiene `downloaded_bytes` y `updated_at`
- [ ] Backend: endpoint de estadísticas agregadas
- [ ] Frontend: renderizar bento card "Total Bandwidth"

---

## 10. Play / Folder Abrir Archivo

| Ítem | Estado | Requisitos |
|------|--------|------------|
| Endpoint `GET /files/{task_id}/download` | 🟡 | Servir archivo estático desde `DOWNLOAD_PATH`. Stream directo |
| Botón Play → abrir reproductor | 🟡 | Frontend: `window.open()` o reproducción in-browser |
| Botón Folder → abrir ubicación | 🔴 | No es posible desde web. Alternativa: copiar ruta al portapapeles o servir ZIP |

**Checklist:**
- [ ] Backend: endpoint de descarga/serve de archivo completado
- [ ] Frontend: botón "Play" abre archivo en nueva pestaña
- [ ] Frontend: botón "Folder" copia ruta al clipboard

---

## 11. Add URL (Descarga por URL)

| Ítem | Estado | Requisitos |
|------|--------|------------|
| Input URL + botón "Add URL" en sidebar | 🟢 | HTML ya existe. Modal o input inline |
| Backend `POST /download/url` | 🔴 | Recibir URL, validar, encolar descarga |
| Integración con yt-dlp / aria2 | 🔴 | Nuevo worker en bot para descargas HTTP/S |
| WebSocket broadcast de progreso | 🟡 | Reusar `ConnectionManager.broadcast()` existente |

**Checklist:**
- [ ] Agregar `yt-dlp` u otra lib a `pyproject.toml`
- [ ] Backend: endpoint `POST /tasks/url` que cree tarea
- [ ] Bot: nuevo worker de descarga por URL
- [ ] Frontend: modal/botón "Add URL" + feedback

---

## 12. Página de Settings

| Ítem | Estado | Requisitos |
|------|--------|------------|
| Ruta/servir página Settings | 🟡 | Nueva ruta `/settings` en FastAPI |
| Formulario de configuración (ALLOWED_USERS, DOWNLOAD_PATH, etc.) | 🔴 | Requiere persistencia de config en DB o archivo, reinicio de servicios |
| Botón "Manage Storage" | 🟡 | Enlace a acción de cleanup/migrate |

**Checklist:**
- [ ] Backend: endpoint config API
- [ ] Backend: persistencia de settings
- [ ] Frontend: formulario + guardado

---

## 13. Autenticación

| Ítem | Estado | Requisitos |
|------|--------|------------|
| Auth middleware en API | 🔴 | Actualmente todos los endpoints son públicos. Agregar JWT o API Key |
| Login page | 🔴 | Nueva ruta + formulario + token storage |
| Proteger WebSocket | 🔴 | Validar token en conexión WS |

> ⚠️ Actualmente la API no tiene ningún tipo de autenticación. Si se expone públicamente, esto es crítico.

**Checklist:**
- [ ] Decidir esquema (API Key en header vs JWT)
- [ ] Backend: middleware de autenticación
- [ ] Frontend: login flow
- [ ] Frontend: attach token a fetch/WS

---

## Resumen de Prioridades

| Prioridad | Features | Esfuerzo |
|-----------|----------|----------|
| **P0** (ahora) | 1. Dashboard nuevo, 2. Iconos, 3. Badges/Progress | Horas |
| **P1** (próximo) | 4. Filtros sidebar, 5. Velocidad, 6. Storage status, 7. Búsqueda | 1-2 días |
| **P2** (corto plazo) | 8. Resume/Pause All, 9. Bandwidth stats, 10. Play/Folder | 2-3 días |
| **P3** (medio plazo) | 11. Add URL, 12. Settings | 1-2 semanas |
| **P4** (largo plazo) | 13. Autenticación | Variable |

---

*Documento generado a partir del diseño en `api/code.html` y análisis del código existente.*
