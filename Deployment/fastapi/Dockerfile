# Base image
FROM python:3.12-slim

# set a working directory
WORKDIR /app

# lightgbm needs libgomp1 (OS-level dependency) before it can import
# --- 1. apt metadata is downloaded --- #
# --- 2. package is installed --- #
# --- 3. apt metadata is deleted --- #
# We delete metadata because it's not required at runtime. 
# If we don't, then it will increase size of the image unnecessarily.
RUN apt-get update \    
 && apt-get install -y --no-install-recommends libgomp1 \
 && rm -rf /var/lib/apt/lists/*

# copy dependencies
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy your application code
COPY . .

# expose the port
EXPOSE 8000

# define the start command
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]