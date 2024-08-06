FROM python:3.12-slim AS base
ARG POETRY_VERSION=1.8.2 
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_CACHE_DIR="/opt/.cache" \
    POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:${PATH}"
WORKDIR /usr/src/app

FROM base AS build-venv
COPY pyproject.toml ./
RUN pip install poetry==${POETRY_VERSION} && \
    poetry install --only=main --no-root --no-ansi

FROM base AS final
ENV PORT=8501
EXPOSE ${PORT}
COPY --from=build-venv /app/.venv ./.venv
COPY . .
ENTRYPOINT .venv/bin/streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl --fail http://localhost:${PORT}/_stcore/health || exit 1
