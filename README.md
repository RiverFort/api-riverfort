# riverfort
The riverfort is the RESTful API application built using the Django REST framework.

## Installation
* `venv`
  * `python3 -m venv ~/.virtualenvs/api_dev`
  * `source ~/.virtualenvs/api_dev/bin/activate`
* `pip install -r /path/to/requirements.txt`

## Development server
  * Modify the `HOST` annotation of `company_db` to `127.0.0.1` (dev).
```
DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': BASE_DIR / 'db.sqlite3',
    },
    'auth_db': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': BASE_DIR / 'db.sqlite3',
    },
    'company_db': {
        'ENGINE': 'django.db.backends.{}'.format(
            env('RIVERFORT_DATABASE_ENGINE')
        ),
        'NAME': env('RIVERFORT_DATABASE_NAME'),
        'USER': env('RIVERFORT_DATABASE_USER'),
        'PASSWORD': env('RIVERFORT_DATABASE_PASSWORD'),
        # prod:
        # 'HOST': '172.17.0.2',
        # dev:
        'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}
```
  * Run `python manage.py runserver`. Navigate to http://127.0.0.1:8000/.
  
## Superuser (Django administration)
  * email: admin@admin.com
  * password: hello

## Dockerisation
* Modify the `HOST` annotation of `company_db` to `172.17.0.2` (prod).
```
DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': BASE_DIR / 'db.sqlite3',
    },
    'auth_db': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': BASE_DIR / 'db.sqlite3',
    },
    'company_db': {
        'ENGINE': 'django.db.backends.{}'.format(
            env('RIVERFORT_DATABASE_ENGINE')
        ),
        'NAME': env('RIVERFORT_DATABASE_NAME'),
        'USER': env('RIVERFORT_DATABASE_USER'),
        'PASSWORD': env('RIVERFORT_DATABASE_PASSWORD'),
        # prod:
        'HOST': '172.17.0.2',
        # dev:
        # 'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}
```
* `docker build -t <username_docker>/riverfort-api:<version> .`
* `docker push <username_docker>/riverfort-api:<version>`
* Example:
  * `docker build -t rgctech/riverfort-api:v2.2.0 .`
  * `docker push rgctech/riverfort-api:v2.2.0`

## Deployment
* Connect to riverfort-api instance
* `docker run -d --name riverfort-api-<version> -p 80:8000 <username_docker>/riverfort-api:<version>`
* Example:
  * `docker run -d --name riverfort-api-v2.0.0 -p 80:8000 rgctech/riverfort-api:v2.2.0`
* Update the CHANGELOG.md
