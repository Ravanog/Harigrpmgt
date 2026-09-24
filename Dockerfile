# Use an official Python runtime as a lightweight parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file first to leverage Docker layer caching
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot's code into the container
COPY . .

# Command to run your bot application
CMD ["python", "bot.py"]
