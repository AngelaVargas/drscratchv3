requirements:
	pip install -r requirements.txt

translate:
	django-admin.py makemessages

coverage:
	coverage run --source='.' manage.py test app

environment:
	export $(cat .env)

build:
	sudo docker-compose build

start:
	sudo docker-compose up


