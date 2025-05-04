FROM ghcr.io/astral-sh/uv:0.6.14-python3.10-bookworm

WORKDIR /app

# Install additional system dependencies for lxml and other packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libavif-dev pkg-config \
    libjpeg-dev \
    gcc unzip zip \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*
    #best practice to clean up the apt cache to minimize the image size

COPY src/requirements.txt .

RUN uv pip install -r requirements.txt --system

COPY src/ .

# create directory for alembic migrations
RUN mkdir -p /app/models/db_shemas/rag   

# copy alembic.ini file to the container
COPY docker/rag/alembic.ini /app/models/db_shemas/rag/
 
COPY docker/rag/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]

#COMMAND TO RUN THE CONTAINER

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000","--workers", "4"]
