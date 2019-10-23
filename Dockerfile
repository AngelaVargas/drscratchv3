FROM python:2-onbuild

LABEL maintainer="cdchushig <cdavid.chushig@gmail.com>"

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir /var/www
WORKDIR /var/www
ADD . /var/www/

# Install dependencies
RUN apt-get update && apt-get install -y libmysqlclient-dev
RUN apt-get install -y texlive-latex-recommended && apt-get clean

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /var/www/app/certificate
RUN chmod +x /var/www/entrypoint.sh

ENTRYPOINT ["/var/www/entrypoint.sh"]

EXPOSE 8000
