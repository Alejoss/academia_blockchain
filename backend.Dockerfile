### Build and install packages
FROM python:3.8

# Update and install system dependencies
RUN apt-get update -y \
  && apt-get install -y gettext \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project files into the Docker image
COPY . /app

# Expose the port Django runs on
EXPOSE 8000

# Environment settings
ENV PYTHONUNBUFFERED=1

# This CMD is just a placeholder; actual command will be provided by docker-compose
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
