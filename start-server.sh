#!/usr/bin/env bash
# start-server.sh

# Exit immediately if a command exits with a non-zero status
set -e

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser if it doesn't already exist
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell
fi

# Collect static files
python manage.py collectstatic --noinput

# Start the Django server
exec python manage.py runserver 0.0.0.0:8000
