FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for WeasyPrint if needed later (e.g. libpango, etc)
# For now, just basic setup.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project definition
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy application
COPY app ./app
COPY server.py .

CMD ["uv", "run", "python", "server.py"]
