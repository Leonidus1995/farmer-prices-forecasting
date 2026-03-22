# A Dockerfile is a recipe to create an image

# Base image
FROM python:3.12-slim

# Set a working directory
WORKDIR /app

# Copy dependency files first
COPY requirements.txt .

# Install dependencies
# using --no-chache-dir keeps the image smaller
RUN pip install --no-cache-dir -r requirements.txt 

# Copy your application code
COPY . .

# Expose the port
EXPOSE 8501

# Define the start command
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]

