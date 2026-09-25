# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy and install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port Koyeb/health-check uses (Port 8080)
EXPOSE 8080

# Run the Telegram bot script directly
CMD ["python", "bot.py"]
