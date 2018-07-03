run:
	pipenv run python manage.py run

psql:
	docker exec -ti $(docker ps -aqf "name=users-db") psql -U postgres

bash:
	docker exec -ti $(docker ps -aqf "name=users-svc") /bin/bash
