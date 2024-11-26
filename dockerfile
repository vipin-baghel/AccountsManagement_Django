# Use an official Python runtime as a parent image
FROM python:3.13-slim-bullseye

# Set the working directory in the container
WORKDIR /finance_management_app

# Copy the current directory contents into the container at /app
COPY . /finance_management_app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the database migrations 
RUN python manage.py makemigrations
RUN python manage.py migrate

# Create superuser, creds will be taken from env variables
RUN python manage.py createsuperuser --noinput

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
