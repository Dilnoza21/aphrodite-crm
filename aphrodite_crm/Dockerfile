# Aphrodite Dress CRM — Docker image
FROM python:3.12-slim

# Where the app lives inside the container
WORKDIR /app

# Install Python dependencies first (better build caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project in
COPY . .

# Build the SQLite database inside the image
RUN python seed_db.py

# The app listens on port 5000
EXPOSE 5000

# Start the server
CMD ["python", "app.py"]
