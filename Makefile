DEPLOY_HOST = app-1.studiotwist.co

.PHONY:
build:
	sudo docker build -t makrub/mkcore .

dev:
	sudo docker run \
		-it \
		-p 8000:8000 \
		-v ${PWD}:/app \
		-e "APP_ENV=local" \
		-e "VAULT_TOKEN=${VAULT_TOKEN}" \
		makrub/mkcore \
		/usr/local/bin/uwsgi --http :8000 --chdir /app/makrub --wsgi-file /app/makrub/config/wsgi.py --py-autoreload 1

migrate:
	sudo docker run \
		-it \
		-e "VAULT_TOKEN=${VAULT_TOKEN}" \
		makrub/mkcore \
		python makrub/manage.py migrate

createsuperuser:
	sudo docker run \
		-it \
		-e "VAULT_TOKEN=${VAULT_TOKEN}" \
		makrub/mkcore \
		python makrub/manage.py createsuperuser
