#!/bin/bash

echo Creando migraciones


echo "yes" | python manage.py flush

rm -rf */migrations

python manage.py makemigrations category product account reports social_django core
python manage.py migrate

# echo ---------------------------------------
# echo -- Llenando Cateogrias/ Sub/ Filtros --
# echo ---------------------------------------

python manage.py loaddata category/initial_data/initial.json

# echo --------------------------------------
# echo --Creando usuario Admin:
# echo -- User: admin
# echo -- password: admin123
# echo --------------------------------------

echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell
