# Geoffrey Homelab & AI Orchestrator [![Docker Image Version (latest by date)](https://img.shields.io/docker/v/toodaniels/geoffrey_telegram?label=ghcr.io/toodaniels/geoffrey_telegram&sort=date)](https://github.com/toodaniels/geoffrey_telegram/pkgs/container/geoffrey_telegram)

A comprehensive media management, streaming, and home automation system, orchestrated by autonomous AI agents.

## System Architecture

This homelab setup utilizes a hybrid architecture:

### 🐳 Containerized Services (`docker-compose`)
- **Geoffrey-bot**: Telegram-based media management & downloader.
- **Jellyfin**: High-performance streaming server.
- **Syncthing**: Seamless file synchronization.
- **HomeAssistant**: Unified smart home automation.

### 🧠 AI Orchestration (Host-based)
- **OpenCode**: Autonomous development and system maintenance agent.
- **Gemini**: Primary intelligence layer for orchestration and automation tasks.

## Getting Started

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Telegram Developer Account

### 2. Deployment
1. Clone the repository:
   ```bash
   git clone [REPOSITORY_URL]
   cd geoffrey_telegram
   ```

2. Setup your `.env` file (see examples).

3. Deploy containerized services:
   ```bash
   docker-compose up -d
   ```

4. Ensure your host environment is configured for the AI agents (OpenCode/Gemini).

## Features

- 📥 Automated media downloading via Telegram
- 🎬 High-performance streaming with Jellyfin
- 🏠 Comprehensive smart home control with HomeAssistant
- 🔄 Seamless data synchronization via Syncthing
- 🤖 AI-driven system maintenance and development orchestration

## Configuration

Refer to individual service documentation for detailed configuration. The primary configuration is managed via `.env` files in the root and service directories.

## File Structure

```
geoffrey_telegram/
├── geoffrey_bot.py      # Main bot code
├── docker-compose.yml   # Homelab services configuration
├── AGENTS.md            # Agent workflow documentation
├── .env                 # Environment configuration
├── downloads/           # Shared media directory
├── sync/                # Syncthing data
├── homeassistant/       # HomeAssistant data
└── ...
```

## License

[MIT License](LICENSE)
