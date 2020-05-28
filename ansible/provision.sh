#!/usr/bin/env bash

APACHE_SERVICE=${1:-'apache2'}

sudo apt update -q
sudo apt upgrade -y
sudo apt autoclean

sudo apt install debconf-utils

sudo apt install python-pip -y
sudo apt install python-dev -y

# Database
sudo apt install libmysqlclient-dev libpq-dev -y

# Library for certificates
sudo apt install texlive-latex-recommended gettext -y

mkdir /home/vagrant/.virtualenvs

sudo pip install --upgrade pip
sudo pip install virtualenv
sudo pip install pipenv
sudo pip install virtualenvwrapper

if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi

#### Start, Enable Service
systemctl start ${APACHE_SERVICE}.service
systemctl enable ${APACHE_SERVICE}.service

