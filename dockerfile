# Use an official Python runtime as a parent image
FROM python:3.13-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for superuser creation
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=admin

# Run the database migrations and create superuser
RUN python manage.py makemigrations 
RUN python manage.py migrate 
RUN python manage.py createsuperuser --noinput

# Generate initial data
RUN python manage.py generate_projects
RUN python manage.py generate_transactions

# Collect static files
RUN python manage.py collectstatic


# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the  server 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

