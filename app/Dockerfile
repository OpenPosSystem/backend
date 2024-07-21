# Use the official Python image from the Docker Hub with Python 3.12.4
FROM python:3.12.4-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y make

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file into the image
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /usr/src/app/

# Expose the port the app runs on
EXPOSE 8000

# Set the default command
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]