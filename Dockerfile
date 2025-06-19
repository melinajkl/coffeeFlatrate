# Use the official lightweight Python image. -> base image
FROM python:3.11-slim 

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Copy only the requirements first to leverage Docker cache -> dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the app into the container
COPY . .

# Expose the FastAPI default port
EXPOSE 8000

# Command to run the app -> entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
