FROM python:3.11-slim

ENV PYTHON_VERSION=3.11
WORKDIR /ML_templete

# 必要最小限のパッケージのインストール
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN pip install poetry

# pyproject.tomlとpoetry.lockをコピー
COPY pyproject.toml poetry.lock* ./

# Poetryを使用して依存関係のインストール
RUN poetry config virtualenvs.create false 

RUN poetry install --no-interaction --no-ansi