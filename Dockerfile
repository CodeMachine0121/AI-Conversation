FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DATABASE_URL "postgresql://myuser:mypassword@postgres:5432/playms_homework"

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    postgresql-client \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r ./requirements/local.txt

# requirements/local.txt 已更新，请重新构建镜像

