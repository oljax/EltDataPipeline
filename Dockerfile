FROM python:3.11-slim

# 1. Install system build dependencies required to compile PostgreSQL packages
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /dbt

# 2. Upgrade pip to ensure the modern dependency resolver works correctly
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 3. Install your exact required dbt core and postgres adapter packages
RUN pip install --no-cache-dir dbt-core==1.8.0 dbt-postgres==1.8.0

# 4. Keeps the container awake safely on macOS
CMD ["tail", "-f", "/dev/null"]
