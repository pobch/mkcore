#!/bin/sh

echo "Running database migrations ..."
python manage.py migrate
echo "Successfully migrated database"

echo "Collecting static files"
python manage.py collectstatic --noinput

if [ "$APP_ENV" == "local" ]; then
    /usr/local/bin/uwsgi --http :8000 --wsgi-file config/wsgi.py --py-autoreload 1
else
    /usr/local/bin/uwsgi --http :8000 --wsgi-file config/wsgi.py
fi
