
ES_URL = localhost:9200

ifdef OS
	docker_build = docker compose up -d --build
	docker_down = docker compose down
else
	docker_build = sudo docker compose up -d --build
	docker_down = sudo docker compose down
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
	curl -XGET $(ES_URL)

del-map:
	curl -XDELETE "$(ES_URL)/map"

get-map:
	curl -XGET "$(ES_URL)/map?pretty"
	


check:
	curl -XPOST '$(ES_URL)/_analyze?pretty' -H 'Content-Type: application/json' -d '{"text": "администратор", "analyzer": "russian"}'

get1:
	curl -XGET "$(ES_URL)/map/_doc/______ind______?pretty"


all:
	curl -XGET '$(ES_URL)/map/_search?scroll=10m&size=50&pretty' -H 'Content-Type: application/json' -d '{"query" : {"match_all" : {}}}'

noacii:
	curl -XGET "$(ES_URL)/_analyze?pretty&analyzer=russian&text=%D0%92%D0%B5%D1%81%D0%B5%D0%BB%D1%8B%D0%B5%20%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B8%20%D0%BF%D1%80%D0%BE%20%D0%BA%D0%BE%D1%82%D1%8F%D1%82" 

w:
	curl -XGET 'localhost:9200/index19/_analyze?analyzer=standard&pretty' -d '%D0%92%D0%B5%D1%81%D0%B5%D0%BB%D1%8B%D0%B5%20%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B8%20%D0%BF%D1%80%D0%BE%20%D0%BA%D0%BE%D1%82%D1%8F%D1%82' -H 'Content-Type: application/octet-stream'