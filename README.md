# Esquel vende

#### Instalación de PostgreSQL

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

```bash
$ sudo su
$ su - postgres
```

Interprete de postgreSQL
```
$ psql
``` 
Cambiamos contraseña de usuario postgres
```
postgres=# \password postgres
postgres=# \q
```

Creamos un servidor, usuario y una base de datos. Esto se puede hacer con [Pgadmin](https://www.pgadmin.org/) o desde ```psql```.

##### Pgadmin

```bash 
$ sudo apt install pgadmin3
```

###### Servidor

1. Add a connection to server.
	* Name = local
	* Host = localhost
	* Port = 5432
	* Username = postgres

###### Usuario

1. Server Groups
2. Servers
3. local(localhost:5432)
4. Login Roles (Click derecho New Login Roles)
	* Properties
		* Role Name = esquelvende
	* Definition:
		* Password = esquelvende

###### Base de datos

1. Server Groups
2. Servers
3. local(localhost:5432)
4. Databases (Click derecho New database)
	* Properties
		* Name = esquelvende
		* Owner = esquelvende
	* Definition:
		* Collaction = es_AR.UTF-8
		* Character type = es_AR.UTF-8


Ultimo ingresan al entorno virtual e instalan los requerimientos.


[Manual postgresql](https://www.postgresql.org/files/documentation/pdf/9.2/postgresql-9.2-A4.pdf)
