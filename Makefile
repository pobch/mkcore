DEPLOY_HOST = app-1.studiotwist.co

dev:
	gunicorn --chdir $(PWD)/makrub config.wsgi:application --reload

migrate:
	./makrub/manage.py makemigrations
	./makrub/manage.py migrate

start:
	gunicron --chdir /app/mkcore-prod makrub.wsgi.application

deploy:
	rsync -avz -e "ssh -o StrictHostKeyChecking=no" ktapi ubuntu@${DEPLOY_HOST}:/app/ktapi-$(env)
