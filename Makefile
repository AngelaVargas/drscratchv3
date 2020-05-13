requirements:
	pip install -r requirements.txt

static:
	docker exec -it drscratchv3_django python manage.py flush --no-input
	docker exec -it drscratchv3_django python manage.py collectstatic --no-input --clear

translate:
	docker exec -it drscratchv3_django python manage.py makemessages -l tr
	docker exec -it drscratchv3_django python manage.py compilemessages

coverage:
	coverage run --source='.' manage.py test app

environment:
	export $(cat .env)

build:
	docker-compose build

start:
	docker-compose up

stop:
	docker-compose down


