# Set up based on Python 3.12-slim image (includes minimal libraries)
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy the local requirements.txt file to the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the current directory to the working directory in the container
COPY . .

# Execute 'run.py' when the container starts
CMD ["python", "run.py"]
