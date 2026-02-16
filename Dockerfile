FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies first (cached layer)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy source
COPY bot.py constants.py handlers.py keyboards.py ./

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app /app

CMD ["/app/.venv/bin/python", "bot.py"]
