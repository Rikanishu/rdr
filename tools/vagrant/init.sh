#!/usr/bin/env bash

DB_USER='rdr'
DB_PASSWORD='rdr'
DB_NAME='rdr'

apt-get update --fix-missing
apt-get install -q -y cowsay python-software-properties python python-pip python-virtualenv g++ make git curl
apt-get install -q -y postgresql
apt-get install -q -y python-psycopg2 libpq-dev libjpeg-dev libxml2-dev libxslt1-dev python-dev libffi-dev
apt-get install -q -y redis-server
apt-get install -q -y nodejs npm nodejs-legacy
apt-get install -q -y wkhtmltopdf

# install elasticsearch / optional
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.1.deb
dpkg -i elasticsearch-1.3.1.deb

npm install -g less uglify uglifycss

sudo -u postgres -i psql postgres -c "CREATE DATABASE $DB_NAME ENCODING 'UTF-8';"
sudo -u postgres -i psql postgres -c "CREATE USER $DB_USER WITH password '$DB_PASSWORD';"
sudo -u postgres -i psql postgres -c "GRANT ALL privileges ON DATABASE $DB_NAME TO $DB_USER;"
sudo -u postgres -i psql $DB_NAME -f dump.sql

cowsay "Your development environment is ready!"
