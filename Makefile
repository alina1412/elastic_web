
ifdef OS
	docker_build = docker compose up -d --build
	docker_down = docker compose down
else
	docker_build = sudo docker-compose up -d --build
	docker_down = sudo docker-compose down
endif

build:
	$(docker_build) 
	

down:
	$(docker_down)

logs:
	docker-compose logs

app:
	docker-compose build backend
	docker-compose up -d backend


renew:
	poetry run alembic -c alembic.ini downgrade -1
	poetry run alembic -c alembic.ini upgrade head

test:
	make renew
	poetry run pytest -m my --verbosity=2 --showlocals


lint:
	poetry run isort backend
	poetry run black backend
# poetry run pylint service

req:
	poetry export -f requirements.txt --without-hashes --with dev --output requirements.txt

req-without-dev:
	poetry export -f requirements.txt --without-hashes --without dev --output backend/service/requirements.txt

ping:
	curl -XGET localhost:9200