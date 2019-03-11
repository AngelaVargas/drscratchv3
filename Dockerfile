FROM python:2-onbuild

LABEL maintainer="cdchushig <cdavid.chushig@gmail.com>"

RUN mkdir /var/www

WORKDIR /var/www

ADD . /var/www/

RUN pip install --upgrade pip && pip install -r requirements.txt

#EXPOSE 8000

