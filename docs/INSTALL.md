### Installation ###

Provided commands are actual for Debian 7 / Ubuntu Server 12.04.
Also you can use included Vagrantfile for instant deploying of development environment via Vagrant.

#### Debian 7 / Ubuntu Server 12.04 ####

1. Install system dependings

  ```
  # python system requirements
  apt-get install -q -y python-software-properties python python-pip g++ make
  
  # installing database
  apt-get install -q -y postgresql
  
  # dependings for pip requirements
  apt-get install -q -y python-psycopg2 libpq-dev libjpeg-dev libxml2-dev libxslt1-dev python-dev libffi-dev
  
  # memory cache
  apt-get install -q -y redis-server
  
  # node js for less compile
  apt-get install -q -y nodejs npm nodejs-legacy
  
  # pdf printing
  apt-get install -q -y wkhtmltopdf
  ```

2. **(Optional)** Download and install ElasticSearch search engine for content indexing. Application uses database SQL LIKE search by default and you can skip this step if you don't want to use separated search engine.

  ```
  wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.1.deb
  dpkg -i elasticsearch-1.3.1.deb
  ```

3. Install LESS compiler

  ``` npm install -g less ```

4. **(For production environment)** Install uglifyjs / uglifycss for static builds making

  ``` npm install uglify uglifycss ```

5. Create new database and user for application

  ```
  sudo -u postgres -i psql postgres -c "CREATE DATABASE rdr ENCODING 'UTF-8';"
  sudo -u postgres -i psql postgres -c "CREATE USER rdr WITH password 'rdr';"
  sudo -u postgres -i psql postgres -c "GRANT ALL privileges ON DATABASE rdr TO rdr;"
  ```

6. Install application pip requirements.

  ```
  pip install -r ./requirements.txt
  ```

7. Configure application.
  
  Default system config is placed in *rdr/application/configs/defaults.py*.
  You can create your own application config and overwrite some configs settings, just copy *example.py* to *app.py* for it, or extend ProductionConfig / DevelopmentConfig for your needs.

  ```
  cp ./rdr/applicaiton/configs/example.py ./rdr/application/configs/app.py
  ```

8. **(For development environment)** Devlopment environment is ready. You can start applciation dev server by command ``` cd /path/to/app && python ./run_app.py ```. Also you may need to run Celery workers or Celerybeat instance to check some functional. You can use the following commands to run celery workers or celery beat manually:
  
  ```
  celery worker -A rdr.tasks.celery -l info -P prefork -c 16
  ```
  ```
  celery beat -A rdr.tasks.celery
  ```

9. **(For production environment)** You can use *tools/uwsgi/* examples to deploy production UWSG application and *tools/supervisor* for examples of supervisor configs. It must run three process. First is application that handles user request, second is a pool of Celery workers and third is a Celerybeat instance for regular updating task.
