# Use a lightweight Python base image
FROM python:3.11-slim

# Create working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port Flask will listen on
EXPOSE 8080

# Command to run Flask on Cloud Run
# We typically bind to 0.0.0.0 so Cloud Run can route traffic internally
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
