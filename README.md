Python/Django admin dashboard + Google Calendar API
================================

### Technical Stack

	- Python/Django: python 3.6, Django 1.11

	- Database: PostgreSQL

### Preinstall

```
  $ export LANGUAGE="en_US.UTF-8"
  $ sudo apt-get install build-essential libssl-dev libffi-dev python-dev
  $ sudo apt-get install zlib1g-dev libjpeg-dev
  $ sudo apt-get install build-essential checkinstall
```

### Python3.6 env

  ```
  $ sudo add-apt-repository ppa:jonathonf/python-3.6
  $ apt-get update

  $ apt-get install python3.6

  $ apt-get install python3-pip
  ```

### Create server

	```
	$ python3.6 -m venv env3

	or

	$ python3.6 -m venv env3 --without-pip

	$ source env3/bin/activate

	$ pip install django==1.11 psycopg2

	$ pip freeze > requirements.txt

	$ django-admin startproject google_calendar_events_manager .
	```

### Get static files

	```
	$ python manage.py collectstatic
	```

### Migrate models into database
	```
	$ python manage.py makemigrations
	```

### Create admin user on server

	```
	$ python manage.py migrate

	$ python manage.py createsuperuser
	```

### Run server
	```
	$ python manage.py runserver

  or

  $ python manage.py runserver 0.0.0.0:8000
	```

### Server urls

- admin page: http://127.0.0.1:8000/admin

In the case you run server with `0.0.0.0:8000` option
- https://192.168.1.120:8000/admin


### Troubleshooting
- Remove migration files
	After faking the migrations for all apps we need to delete the migrations files inside migrations folder in each app.

	You can use the previous bash script to automate this process in Unix bases OSs.

	```
	$ find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	$ find . -path "*/migrations/*.pyc"  -delete
	```
	This will delete Python source files and also compiled Python files for migrations except for the special Python file init.py

- Make migrations again
	Now you need to re-create the initial database migrations with the usual commands
	```
	$ python manage.py makemigrations
	```

# Deployinig
- Global server: Heroku
- URL: https://gceventmanager.herokuapp.com/admin
- Admin user name: admin
- Admin password: 123qweasd