# Run Mini blog in Docker container

### Configure .env file

````
SENDGRID_API_KEY = 'your_key'

FROM_EMAIL = 'email'

SECRET_KEY = 'your_app_secret_key'

DEBUG = False

ENGINE = 'django.db.backends.postgresql_psycopg2'

DB_NAME = 'postgres'

DB_USER = 'postgres'

DB_PASSWORD = 'postgres'

DB_HOST = 'postgres'

DB_PORT = 5432

CELERY_BROKER_URL = 'amqp://rabbitmq:5672'

CELERY_RESULT_BACKEND = 'amqp'
````

### Commands

1. `docker-compose up -d --build` - build container and run it.
2. `docker-compose run web python manage.py migrate` - create the database tables.
3. `docker-compose run web python manage.py collectstatic` - collect static files.
4. `docker-compose run web python manage.py loaddata initial_data.json` - populate database with the needed initial data.
5. `docker-compose run web python manage.py createsuperuser` - create an admin user for the website.
6. `docker-compose stop` - stop container.
7. `docker-compose down -v` - stop and delete all containers.
 
 Setup [authentication](https://django-allauth.readthedocs.io/en/latest/installation.html "Django allauth") through Google.
 
