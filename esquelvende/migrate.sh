#!/bin/bash

echo Creando migraciones

if [ -f "db.sqlite3" ]; then
    rm db.sqlite3
fi

rm -rf */migrations
python manage.py makemigrations categories products reports favorites last_seen social_django users
python manage.py migrate

echo ---------------------------------------
echo -- Llenando Cateogrias/ Sub/ Filtros --
echo ---------------------------------------

python manage.py loaddata categories/initial_data/initial.json

echo --------------------------------------
echo --Creando usuario Admin:
echo -- User: admin
echo -- password: admin123
echo --------------------------------------

echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell
