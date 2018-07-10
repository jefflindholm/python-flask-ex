start:
	docker-compose -f docker-compose-dev.yml up -d --build
lint:
	docker-compose -f docker-compose-dev.yml run users flake8 project
coverage:
	docker-compose -f docker-compose-dev.yml run users python manage.py cov
test:
	docker-compose -f docker-compose-dev.yml run users python manage.py test
seed_db:
	docker-compose -f docker-compose-dev.yml run users python manage.py seed_db
recreate_db:
	docker-compose -f docker-compose-dev.yml run users python manage.py recreate_db

db: recreate_db seed_db
