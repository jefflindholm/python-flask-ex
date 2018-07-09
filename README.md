# Microservice with Docker, Flask, and UI

[![Build Status](https://travis-ci.org/jefflindholm/testdriven-app.svg?bran
ch=master)](https://travis-ci.org/jefflindholm/testdriven-app)


* start
`docker-compose -f docker-compose-dev.yml up --build`
* lint
`docker-compose -f docker-compose-dev.yml run users flake8 project`
* coverage
`docker-compose -f docker-compose-dev.yml run users python manage.py cov`
* test
`docker-compose -f docker-compose-dev.yml run users python manage.py test`
* seed_db
`docker-compose -f docker-compose-dev.yml run users python manage.py seed_db`
* recreate db
`docker-compose -f docker-compose-dev.yml run users python manage.py recreate_db`
