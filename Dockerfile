# syntax=docker/dockerfile:1

FROM python:3.13-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN pip install --no-cache-dir uv==0.9.17

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
RUN uv sync --frozen --no-dev --no-editable


FROM python:3.13-slim

RUN groupadd --system task-analyzer \
    && useradd --system --gid task-analyzer --create-home task-analyzer

WORKDIR /app

COPY --from=builder --chown=task-analyzer:task-analyzer /app/.venv ./.venv

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1

USER task-analyzer

EXPOSE 8000

CMD ["uvicorn", "task_analyzer_server.app:application_factory", "--factory", "--host", "0.0.0.0", "--port", "8000"]
