# Use official Python base image
FROM python:3.11-slim

# Install system dependencies required by opencv and pillow-heif
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libheif1 \
    libde265-0 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Poetry and project dependencies
ENV POETRY_VERSION=2.1.4
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Copy project files
COPY . /app

# Set the port for Cloud Run
ENV PORT=8080
EXPOSE 8080

# Start the web server
CMD ["sh", "-c", "uvicorn herbarium_processor.web.main:app --host 0.0.0.0 --port ${PORT}"]
