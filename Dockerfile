FROM python:2-onbuild

LABEL maintainer="cdchushig <cdavid.chushig@gmail.com>"

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir /var/www
WORKDIR /var/www
ADD . /var/www/

# Install Mysql dependencies
RUN apt-get update && apt-get install -y libmysqlclient-dev && apt-get clean

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

