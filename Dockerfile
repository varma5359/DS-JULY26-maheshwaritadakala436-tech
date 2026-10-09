
# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show logs immediately
ENV PYTHONUNBUFFERED=1

# Copy dependencies first
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create required directories
RUN mkdir -p logs reports data/cleaned

# Run the analytics pipeline
CMD ["python", "run_pipeline.py"]
