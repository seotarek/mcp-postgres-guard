FROM python:3.11-slim

WORKDIR /app

COPY . /app

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "-m", "mcp_postgres_guard.server"]
