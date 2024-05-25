FROM python:3.12-slim as base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_CACHE_DIR="/opt/.cache" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VERSION=1.8.2 
ENV PATH="$POETRY_HOME/bin:${PATH}"
WORKDIR /app

FROM base as builder
COPY pyproject.toml ./
RUN pip install poetry==${POETRY_VERSION} && \
    poetry install --only=main --no-root --no-ansi

FROM base as final
COPY --from=builder /app/.venv ./.venv
COPY . .
CMD .venv/bin/streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0
