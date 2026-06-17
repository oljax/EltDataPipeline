FROM python:3.8-slim

# 1. Install required helper utilities
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# 2. Securely download and dearmor the official PostgreSQL key
RUN curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
    gpg --dearmor -o /usr/share/keyrings/postgresql-archive-keyring.gpg

# 3. Add the PGDG repository mapped explicitly to your keyring
RUN echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# 4. Update index and install the exact v18 client tools
RUN apt-get update && apt-get install -y \
    postgresql-client-18 \
    && rm -rf /var/lib/apt/lists/*

# Copy the ELT script 
COPY elt_script.py .

# Set the default command to run the ELT script
CMD ["python", "elt_script.py"]