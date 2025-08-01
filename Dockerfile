# Use slim Python 3.11 base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Make startup script executable
RUN chmod +x startup.sh

# Create directory for database if using SQLite
RUN mkdir -p /app/data

# Initialize database tables immediately during build
RUN python3 -c "
from app import create_app, db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.meeting import Meeting
from app.models.notification import Notification

app = create_app()
with app.app_context():
    try:
        db.create_all()
        print('✅ Database tables created successfully during build!')
    except Exception as e:
        print(f'Database initialization error: {e}')
"

# Expose the port your Flask app runs on
EXPOSE 5000

# Use startup script as entrypoint
ENTRYPOINT ["./startup.sh"]