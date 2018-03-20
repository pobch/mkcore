DEPLOY_HOST = app-1.studiotwist.co

dev:
	docker run \
		-it \
		-p 8000:8000 \
		-v $(pwd):/app \
		mkcore \
		/usr/local/bin/uwsgi --http :8000 --chdir /app/makrub --wsgi-file /app/makrub/config/wsgi.py --py-autoreload 1
	gunicorn --chdir $(PWD)/makrub config.wsgi:application --reload

migrate:
	docker run \
		-it \
		-v $(pwd):/app \
		mkcore \
		python makrub/manage.py migrate

start:
	gunicron --chdir /app/mkcore-prod makrub.wsgi.application

deploy:
	rsync -avz -e "ssh -o StrictHostKeyChecking=no" ./ ubuntu@${DEPLOY_HOST}:/app/ktapi-$(env)/
