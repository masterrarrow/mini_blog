# Mini blog on Django

### Setup process
1. Install `python 3.7+` and if you want to create a virtual environment - `pipenv --python 3.7`
2. Inside the root directory run `pipenv shell` and `pip install requirements.txt`
3. Install [redis](https://redis.io/ "Redis") or other message-broker.
4. Create `.env` file with the next data:

````
SENDGRID_API_KEY = 'your_key'

FROM_EMAIL = 'email'

SECRET_KEY = 'your_app_secret_key'

DEBUG = False

CELERY_BROKER_URL = 'url'

ENGINE = 'database engine'

DB_NAME = 'database name'

DB_USER = 'database root user'

DB_PASSWORD = 'database root user password'

DB_HOST = 'database host'

DB_PORT = 0000
````

##### Where:

The default configuration inside the project for the database set for `sqlite3` database. If you want to use another database like `PostgreSQL` or `MySQL` you need to look into its documentation and set the above parameters accordingly.


SENDGRID_API_KEY - Your `SendGrid` API Key. You can get it [here](https://app.sendgrid.com "SendGrid") after a simple registration process.


FROM_EMAIL - Email from which site users going to receive a notification emails.


SECRET_KEY - Secret key for your application.


You can generate it by running in your terminal the next commands:


>> pip install secrets

>> python

>> import secrets

>> secrets.token_hex(16)


DEBUG - `False` or `True` depending on which mode you want to run your application. `False` by default.


CELERY_BROKER_URL - `Redis` or other message-broker manager url. Example: `redis://127.0.0.1:6379/0`.

ENGINE - depends on the database that you using. By default, it configured to support sqlite3 database.

To configure Django to work with another database you need to look into [documentation](https://docs.djangoproject.com/en/3.0/ref/databases/ "Djangoproject docs").

DB_HOST - database addres. For MySQL or PostgreSQL it may look like 127.0.0.1, localhost or any other url addres without http:// or https://.


To run Mini blog in Docker container see [Docker_run.md](https://github.com/masterrarrow/mini_blog/blob/master/Docker_run.md "Docker_run.md")

Checkout the [commands](#commands) section for more usage.

### Commands

After setting up your `.env` file you can run the application. To work it correctly you need to run your message-broker manager and `Celery`.

1. Run the `Celery`.
2. `python manage.py makemigrations && python manage.py migrate` to create the database tables.
3. `python manage.py collectstatic` to collect static files.
4. `python manage.py loaddata initial_data.json` to populate database with the needed initial data.
5. `python manage.py createsuperuser` to create an admin user for the website.
6. `python manage.py runserver` to start the website.
7. Setup [authentication](https://django-allauth.readthedocs.io/en/latest/installation.html "django allauth") through Google.


All information posted by users from `user group` on the site will go through the moderation stage and can by `approved` or `declined` (default=`pending`). You can find the needed tools in the admin dashboard `your_site_url/admin`.

### Possible issues

If you ran into a problem with the admin panel on the site. It doesn’t displays correctly or you can’t reach it at all, it means that your application cannot find a right pass to a static files directory or some files are missing.

To configure static files properly you need to delete a static folder inside the project main directory, then open your console and execute the next command:


`python manage.py collectstatic`


It collects all needed static files for you.

If you need to configure host settings. You need to open file `mini_blog/settings.py` in the project main directory and change the ALLOWED_HOSTS option.


By default, it configured to allow all hosts:


ALLOWED_HOSTS=[‘*’]


This means that your application can be deployed on any host you like. To change it you need instead of ‘*’ write down your hostname, for example:


ALLOWED_HOSTS=[‘my-blog.com’]

#### You can find this project on Heroku by following the link: [Mini blog](https://news-blog-site.herokuapp.com/ "Mini blog").
