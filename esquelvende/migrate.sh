#!/bin/bash

echo Creando migraciones

if [ -f "db.sqlite3" ]; then
    rm db.sqlite3
fi

rm -rf */migrations
python manage.py makemigrations categories products reports users
python manage.py migrate
