FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (if it exists)
COPY requirements.txt* /app/

# Install Python dependencies
RUN pip install --no-cache-dir Django==6.0.2 psycopg2-binary

# Copy project
COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
