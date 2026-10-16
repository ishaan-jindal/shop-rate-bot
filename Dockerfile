FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8000
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
COPY src/ src/
COPY static/ static/
RUN uv sync --locked --no-dev

EXPOSE 8000
CMD ["sh", "-c", ".venv/bin/uvicorn app:app --app-dir src --host 0.0.0.0 --port ${PORT:-8000}"]
