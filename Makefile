requirements:
	pip install -r requirements.txt

static:
    sudo docker exec -it drscratchv3_django python manage.py flush --no-input
    sudo docker exec -it drscratchv3_django python manage.py collectstatic --no-input --clear

translate:
	sudo docker exec -it drscratchv3_django python manage.py makemessages -l tr
	sudo docker exec -it drscratchv3_django python manage.py compilemessages

coverage:
	coverage run --source='.' manage.py test app

environment:
	export $(cat .env)

build:
	sudo docker-compose build

start:
	sudo docker-compose up

stop:
	sudo docker-compose down


