# Arcane — panel web de contenedores

Interfaz web para ver y controlar los contenedores del usuario (`geoffrey-bot`,
`myjellyfin`, `homeassistant`, …) en este servidor.

- **URL LAN:** http://192.168.1.91:3552
- **Primer login:** `arcane` / `arcane-admin` → **cambiar la contraseña en el primer acceso**
- **Gestión:** systemd de usuario (Quadlet), no `podman compose`

## Por qué vive aquí y no en el compose de Geoffrey

- Arcane gestiona *stacks*. Dentro del stack que gestiona, un redeploy lo
  recrearía a sí mismo a mitad de la operación.
- `compose.yml` (bot-only, sin el montaje `/mnt/avivo`) tiene prioridad sobre
  `docker-compose.yml`. Cualquier `podman compose up -d` en la raíz es una
  ruleta para los tres contenedores que ya funcionan.
- Ciclo de vida distinto: actualizar el panel no debe reiniciar descargas ni
  streams.
- `arcane/.env` (clave de cifrado) no se mezcla con el `.env` del bot.

## Cómo está montado

```
~/.config/containers/systemd/arcane.container   -> symlink a este directorio
arcane/arcane.container    unidad (fuente de verdad, en este repo)
arcane/.env                ENCRYPTION_KEY, APP_URL, PROJECTS_DIRECTORY  (chmod 600)
arcane/data/               estado de Arcane: SQLite, config, logs  (gitignored)
arcane/projects/           PROJECTS_DIRECTORY vacío, para stacks nuevos  (gitignored)
```

El symlink es la única pieza fuera de la carpeta: systemd solo lee Quadlets de
`~/.config/containers/systemd/`. El generador **sí sigue symlinks** (verificado).

## Operación

```bash
# estado
systemctl --user status arcane --no-pager

# arrancar / parar / reiniciar
systemctl --user start arcane
systemctl --user stop arcane
systemctl --user restart arcane

# logs
journalctl --user -u arcane -f
podman logs -f arcane

# arranca solo tras reboot? (linger ya está activo)
systemctl --user is-enabled arcane
```

## Actualizar Arcane

Arcane corriendo como Quadlet **no se auto-actualiza** (su botón de update
recrearía el contenedor fuera de systemd):

```bash
podman pull ghcr.io/getarcaneapp/manager:latest
systemctl --user restart arcane
```

Si se fija la imagen por digest en `arcane.container`, actualizar es cambiar el
digest, `systemctl --user daemon-reload` y `restart`.

## Backup

Todo el estado está en `arcane/data/`. Basta con copiar esa carpeta con el
servicio parado. **`arcane/.env` es imprescindible**: sin esa clave, los valores
cifrados de la base de datos no se pueden descifrar.

## Desinstalar

```bash
systemctl --user stop arcane
rm ~/.config/containers/systemd/arcane.container
systemctl --user daemon-reload
podman rm -f arcane && podman rmi ghcr.io/getarcaneapp/manager:latest
# y borrar esta carpeta
```

## Notas y trampas

- **Socket = control total** de todos los contenedores del usuario. Solo LAN.
  Si algún día se expone fuera, poner delante un socket-proxy.
- **`PUID`/`PGID` deliberadamente ausentes.** En podman rootless, `PUID=1000`
  mapea al uid 101000 del host, que no puede leer el socket (propiedad de 1000).
  Dejando el contenedor como root interno, mapea a 1000 y funciona. Si alguna
  versión obliga a bajar privilegios: `UserNS=keep-id` + `PUID=1000`.
- **`git clean -fdx`** en este repo borraría `data/` y `.env` (están ignorados).
- **Si se mueve o renombra esta carpeta**, el symlink queda colgando:
  `ln -sfn <nueva-ruta>/arcane.container ~/.config/containers/systemd/`.
- Arcane no gestiona pods ni Quadlets (limitación de la API Docker-compatible).
- No adopta el compose de Geoffrey: el directorio de proyectos es este
  `arcane/projects/` vacío. Los contenedores existentes se gestionan uno a uno.
