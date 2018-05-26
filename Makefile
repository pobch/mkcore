DEPLOY_HOST = app-1.studiotwist.co

.PHONY:
build:
	sudo docker build -t mkcore .

dev:
	sudo docker run \
		-it \
		-p 8000:8000 \
		-v ${PWD}:/app \
		-e "VAULT_TOKEN=${VAULT_TOKEN}" \
		mkcore \
		/usr/local/bin/uwsgi --http :8000 --chdir /app/makrub --wsgi-file /app/makrub/config/wsgi.py --py-autoreload 1

migrate:
	sudo docker run \
		-it \
		-v ${PWD}:/app \
		mkcore \
		python makrub/manage.py migrate

createsuperuser:
	sudo docker run \
		-it \
		-v ${PWD}:/app \
		mkcore \
		python makrub/manage.py createsuperuser

start:
	gunicron --chdir /app/mkcore-prod makrub.wsgi.application
