dev:
	gunicorn --chdir makrub makrub.wsgi:application --reload

migrate:
	./makrub/manage.py migrate

start:
	gunicron --chdir /app/mkcore-prod makrub.wsgi.application
