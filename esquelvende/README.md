# Esquel Vende.
## Installation

### Requirements
* 0. Python 2.7
* 1. Pip
* 2. Virtualenv
* 3. Postgres

```
    1.
    $ apt install python-pip
    
    2.
    $ sudo pip install virtualenv
    $ mkdir ~/.virtualenvs
    $ sudo pip install virtualenvwrapper
    $ export WORKON_HOME=~/.virtualenvs
    $ source /usr/local/bin/virtualenvwrapper.sh
    
    Cerrar la terminal y volverla abrir.
    $ mkvirtualenv ev
    
    3.
    $ sudo apt-get update
    $ sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
```

### Configuration
Como django tiene bastante soporte con postgres, para nuestro humilde buscador usamos algunas extensiones que 
hay que agregarlas a la base de datos. Asi que vamos a configurar postgres y agregar las extensiones.

```
    $ sudo su - postgres
    $ psql
    
    $ CREATE DATABASE esquelvende;
    $ CREATE USER admin WITH PASSWORD '1234';

    $ ALTER ROLE admin SET client_encoding TO 'utf8';
    $ ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
    $ ALTER ROLE admin SET timezone TO 'UTC';
    $ GRANT ALL PRIVILEGES ON DATABASE esquelvende TO admin;

    $ \c esquelvende;
    $ CREATE EXTENSION unaccent;
    $ CREATE EXTENSION pg_trgm;

    $ \q
    $ exit
```


## Development

```
$ workon ev
$ git clone https://gitlab.com/usernamegit/esquelvendedjango.git

$ pip install -r requirements/requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver

Luego cargar las categorias de la aplicacion:
`python manage.py loaddata category/initial_data/initial.json`
```
