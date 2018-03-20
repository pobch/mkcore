DEPLOY_HOST = app-1.studiotwist.co

dev:
	sudo docker run \
		-it \
		-p 8000:8000 \
		-v ${PWD}:/app \
		mkcore \
		/usr/local/bin/uwsgi --http :8000 --chdir /app/makrub --wsgi-file /app/makrub/config/wsgi.py --py-autoreload 1

.PHONY:
build:
	sudo docker build -t mkcore .

migrate:
	sudo docker run \
		-it \
		-v ${PWD}:/app \
		mkcore \
		python makrub/manage.py migrate

start:
	gunicron --chdir /app/mkcore-prod makrub.wsgi.application

deploy:
	rsync -avz -e "ssh -o StrictHostKeyChecking=no" ./ ubuntu@${DEPLOY_HOST}:/app/ktapi-$(env)/
