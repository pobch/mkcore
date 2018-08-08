#!/bin/sh

echo "Running database migrations ..."
python manage.py migrate
echo "Successfully migrated database"

if [ "$APP_ENV" = "prod" ]; then
    /usr/local/bin/uwsgi --http :8000 --wsgi-file config/wsgi.py
else
    /usr/local/bin/uwsgi --http :8000 --wsgi-file config/wsgi.py --py-autoreload 1
fi
