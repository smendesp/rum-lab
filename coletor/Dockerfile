# FROM python:3.12.11-alpine3.22 AS base
FROM python:3.13.5-alpine3.22 AS base

FROM base AS builder

RUN apk add gcc musl-dev linux-headers

COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY ./uv.lock ./pyproject.toml ./uvicorn_start.sh /app/

RUN --mount=type=cache,target=/root/.cache/uv 

RUN uv sync --frozen --no-install-project --no-dev

COPY ./app /app

# RUN --mount=type=cache,target=/root/.cache/uv
# RUN uv sync --frozen --no-dev

#RUN rm -f ./uv.lock

FROM base

WORKDIR /app

COPY --from=builder /app /tmp/app
# COPY --from=builder /bin/uv /bin/uv

RUN cp -rd /tmp/app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

RUN mkdir app

RUN cp -rd /tmp/app ./

RUN mv ./app/pyproject.toml ./
# RUN mv ./app/uv.lock ./
RUN mv ./app/uvicorn_start.sh ./

RUN rm -rf /tmp/app

RUN python3 -m ensurepip

RUN opentelemetry-bootstrap -a install

EXPOSE 8000

ENV WORKERS="4"

#CMD [ "opentelemetry-instrument", "fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "--workers", "4" ]

#uv run opentelemetry-instrument uvicorn app.main:app
#CMD ["opentelemetry-instrument", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "$WORKERS"]

CMD ["sh", "./uvicorn_start.sh"]
#CMD ["sleep", "infinity"]