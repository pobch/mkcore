DEPLOY_HOST = app-1.studiotwist.co

.PHONY:
build:
	sudo docker build -t makrub/mkcore .

docker-base:
	sudo docker build -t makrub/mkcore-base -f Dockerfile.base .

dev:
	sudo docker run \
		-it \
		-p 8000:8000 \
		-v ${PWD}:/app \
		-v ${PWD}/makrub/.env:/etc/app/.env \
		-e "APP_ENV=local" \
		-e "VAULT_TOKEN=${VAULT_TOKEN}" \
		makrub/mkcore

manage:
	sudo docker run \
		-it \
		-v ${PWD}:/app \
		-v ${PWD}/makrub/.env:/etc/app/.env \
		makrub/mkcore \
		python manage.py ${MANAGE_CMD}

migrate:
	sudo docker run \
		-it \
		-v ${PWD}:/app \
		-v ${PWD}/makrub/.env:/etc/app/.env \
		makrub/mkcore \
		python manage.py migrate

createsuperuser:
	sudo docker run \
		-it \
		-v ${PWD}:/app \
		-v ${PWD}/makrub/.env:/etc/app/.env \
		makrub/mkcore \
		python manage.py createsuperuser
