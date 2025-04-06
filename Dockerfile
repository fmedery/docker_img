# Use an official minimal Python runtime as a parent image
FROM python:3.12.9-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# PORT the app runs on
ENV PORT=9999
# IPINFO_TOKEN can be set during build or runtime
# ARG IPINFO_TOKEN
# ENV IPINFO_TOKEN=${IPINFO_TOKEN}

# Create and set the working directory
WORKDIR /app

# Create a non-root user and group
RUN addgroup --system app && adduser --system --ingroup app app

# Install system dependencies if any (uncomment if needed)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY templates templates

# Change ownership of the app directory
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port the app runs on
EXPOSE ${PORT}

# Command to run the application
# The IPINFO_TOKEN environment variable will be picked up by app.py if set when running the container.
# You can also pass --ipinfo-token='YOUR_TOKEN' or --debug here if needed.
CMD ["python", "app.py"] 