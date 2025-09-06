FROM node:20 AS frontend
WORKDIR /web

# Copy only files needed to install and build (for better caching)
# Adjust the path to your actual frontend root
COPY src/herbarium_processor/web/frontend/package*.json ./
RUN npm ci

COPY src/herbarium_processor/web/frontend/ ./
RUN npm run build
# Result: /web  /dist (index.html + assets)

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

# Install Poetry
ENV POETRY_VERSION=2.1.4
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Copy only dependency files first (better layer caching)
# TODO -- move data/cs_canonical.csv to the prompt directory
COPY pyproject.toml poetry.lock* README.md data/cs_canonical.csv prompts/ /app/
COPY src/ /app/src/

# Install dependencies only; do not install the project package
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Now copy the rest of the project
COPY . /app

# Set the port for Cloud Run
ENV PORT=8080
EXPOSE 8080

# Start the web server
CMD ["sh", "-c", "uvicorn herbarium_processor.web.main:app --host 0.0.0.0 --port ${PORT}"]
