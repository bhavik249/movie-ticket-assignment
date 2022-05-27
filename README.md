# Movie or Concert Ticket 

Assignment to create the RESTful API backend server.

You need to implement locking mechanism for user for certain period of time

- Model (example)
    - Movie
    - Seating
    - Reservations
- API list (example)
    - GET /seatings/
    - POST /seatings/\<id:int>/Lock/
    - POST /seatings/\<id:int>/Purchase/


## Setup

### Create a virtualenv and activate it

```sh
python3 -m venv env
source env/bin/activate
```

### Install dependencies

```sh
poetry install
```

### Set the env variables


```sh
export ENV=dev
export DJANGO_SETTINGS_MODULE=settings.local
export SECRET_KEY=djangosecretkey
export DB_USERNAME=""
export DB_PASSWORD=""
export DB_HOST=""
export REDIS_HOST=""
export S3_BUCKET=""
export SLACK_TOKEN=""
export AWS_DEFAULT_REGION=us-west-2
```

### Migrate the databse

```sh
python manage.py migrate
```

### Run the server

```sh
python manage.py runserver_plus
```

API Authentication: http://127.0.0.1:8000/api-auth/login/

Admin Panel: http://127.0.0.1:8000/nimda/

Swagger: http://127.0.0.1:8000/api/docs/swagger/
