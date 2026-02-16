# Tomakuro

A minimalist Telegram pomodoro timer bot. Start a timer, track your focus sessions, and take breaks — all from a persistent keyboard menu at the bottom of the chat.

## Features

- **Pomodoro Timer** — Pick from 15 / 30 / 45 / 60 / 90 / 120 minute sessions
- **Auto Break** — A break timer starts automatically after each session (default 5 min)
- **Add Time** — Extend a running timer by 5 / 10 / 15 / 30 minutes
- **Live Status** — Check elapsed time, remaining time, and finish time at any moment
- **Settings** — Configure your break duration (3 / 5 / 10 / 15 min)
- **Per-User Sessions** — Each user gets their own independent timer

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

### Run Locally

```bash
# Install dependencies
uv sync

# Set your bot token
export TELEGRAM_BOT_TOKEN="your-bot-token-here"

# Start the bot
uv run python bot.py
```

### Run with Docker

```bash
docker build -t tomakuro .
docker run -e TELEGRAM_BOT_TOKEN="your-bot-token-here" tomakuro
```

### Run with Docker Compose (Recommended for Deployment)

```bash
# Download the compose file and env template
curl -O https://raw.githubusercontent.com/aturret/Tomakuro/main/docker-compose.yml
curl -O https://raw.githubusercontent.com/aturret/Tomakuro/main/.env.example

# Create a .env file with your token
cp .env.example .env
# Edit .env and set TELEGRAM_BOT_TOKEN

# Start the bot
docker compose up -d
```

## Usage

1. Open your bot in Telegram and send `/start`
2. A persistent keyboard appears at the bottom with four buttons:

| Button | Action |
|---|---|
| **Start Clock** | Pick a duration and start a pomodoro |
| **Status** | View current timer or break status |
| **Stop** | Stop the running timer or break |
| **Settings** | Change your break duration |

3. Duration selection and timer actions appear as inline buttons inside messages

## Project Structure

```
Tomakuro/
├── bot.py           # Entry point — handler registration and polling
├── handlers.py      # All handler functions (keyboard, inline, job callbacks)
├── keyboards.py     # Keyboard builders (reply + inline)
├── constants.py     # Button labels, callback data, durations
├── pyproject.toml   # Project config and dependencies
├── uv.lock          # Locked dependency versions
├── Dockerfile         # Multi-stage Docker build
├── docker-compose.yml # Docker Compose config
└── .github/
    └── workflows/
        └── docker.yml  # CI pipeline — build and push Docker image
```

## CI/CD

A GitHub Actions workflow runs on every push to `main`:

1. Builds the Docker image using multi-stage build
2. Pushes to GitHub Container Registry (`ghcr.io`)
3. Tags with `latest` and the commit SHA
4. Uses GitHub Actions build cache for fast rebuilds

## Tech Stack

- **Runtime** — Python 3.12
- **Telegram SDK** — [python-telegram-bot](https://python-telegram-bot.org/) v22 with job queue
- **Package Manager** — [uv](https://docs.astral.sh/uv/)
- **Container** — Docker (Python 3.12-slim)
- **CI** — GitHub Actions
