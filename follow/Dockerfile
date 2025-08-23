FROM python:3.13-alpine

# Install build dependencies for postgres
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libpq-dev \
    postgresql-dev \
    python3-dev

ARG SERVICE_NAME

RUN pip install --upgrade pip && pip install poetry

COPY common /app/common
COPY ${SERVICE_NAME}/pyproject.toml poetry.lock* /app/${SERVICE_NAME}

WORKDIR /app/${SERVICE_NAME}

RUN poetry install --with dev --no-root

COPY . .

CMD ["poetry", "run", "python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

