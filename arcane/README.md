# Arcane — container web panel

Web interface to view and control the user's containers (`geoffrey-bot`,
`myjellyfin`, `homeassistant`, …) on this server.

- **LAN URL:** http://192.168.1.100:3552
- **First login:** `arcane` / `arcane-admin` → **change the password on first access**
- **Management:** user systemd (Quadlet), not `podman compose`

## Why it lives here and not in Geoffrey's compose

- Arcane manages *stacks*. Within the stack it manages, a redeploy would
  recreate itself in the middle of the operation.
- `compose.yml` (bot-only, without the `/mnt/media` mount) takes precedence over
  `docker-compose.yml`. Any `podman compose up -d` in the root is a
  gamble for the three containers that already work.
- Different lifecycle: updating the panel should not restart downloads or
  streams.
- `arcane/.env` (encryption key) is not mixed with the bot's `.env`.

## How it is set up

```
~/.config/containers/systemd/arcane.container   -> symlink to this directory
arcane/arcane.container    unit (source of truth, in this repo)
arcane/.env                ENCRYPTION_KEY, APP_URL, PROJECTS_DIRECTORY  (chmod 600)
arcane/data/               Arcane state: SQLite, config, logs  (gitignored)
arcane/projects/           empty PROJECTS_DIRECTORY, for new stacks  (gitignored)
```

The symlink is the only piece outside the folder: systemd only reads Quadlets
from `~/.config/containers/systemd/`. The generator **does follow symlinks**
(verified).

## Operation

```bash
# status
systemctl --user status arcane --no-pager

# start / stop / restart
systemctl --user start arcane
systemctl --user stop arcane
systemctl --user restart arcane

# logs
journalctl --user -u arcane -f
podman logs -f arcane

# does it start on its own after a reboot? (linger is already active)
systemctl --user is-enabled arcane
```

## Updating Arcane

Arcane running as a Quadlet **does not auto-update** (its update button
would recreate the container outside of systemd):

```bash
podman pull ghcr.io/getarcaneapp/manager:latest
systemctl --user restart arcane
```

If the image is pinned by digest in `arcane.container`, updating means changing
the digest, `systemctl --user daemon-reload`, and `restart`.

## Backup

All the state lives in `arcane/data/`. Copying that folder with the
service stopped is enough. **`arcane/.env` is essential**: without that key, the
encrypted values in the database cannot be decrypted.

## Uninstall

```bash
systemctl --user stop arcane
rm ~/.config/containers/systemd/arcane.container
systemctl --user daemon-reload
podman rm -f arcane && podman rmi ghcr.io/getarcaneapp/manager:latest
# and delete this folder
```

## Notes and pitfalls

- **Socket = full control** over all of the user's containers. LAN only.
  If it is ever exposed outside, put a socket-proxy in front of it.
- **`PUID`/`PGID` deliberately absent.** In rootless podman, `PUID=1000`
  maps to host uid 101000, which cannot read the socket (owned by 1000).
  Leaving the container as internal root maps to 1000 and works. If some
  version forces dropping privileges: `UserNS=keep-id` + `PUID=1000`.
- **`git clean -fdx`** in this repo would delete `data/` and `.env` (they are ignored).
- **If this folder is moved or renamed**, the symlink dangles:
  `ln -sfn <new-path>/arcane.container ~/.config/containers/systemd/`.
- Arcane does not manage pods or Quadlets (a limitation of the Docker-compatible API).
- It does not adopt Geoffrey's compose: the project directory is this
  empty `arcane/projects/`. Existing containers are managed one by one.
