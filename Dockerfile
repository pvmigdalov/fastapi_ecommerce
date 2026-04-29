FROM python:3.13.13-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=0 \
    UV_LINK_MODE=copy

WORKDIR /fastapi_ecommerce

RUN apt update && apt upgrade -y
# RUN apt install -y curl

# RUN pip install uv
# RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

COPY ./ ./

CMD ["uv", "run", "python", "-m", "app.main"]