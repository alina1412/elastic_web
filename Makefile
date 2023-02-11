
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
	curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_cluster/settings -d '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
	curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'

down:
	$(docker_down)

logs:
	docker-compose logs

app:
	docker compose build backend
	docker compose up -d backend


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

#ping elastic
ping:
	curl -XGET $(ES_URL)

#del only index named "map"
del-map:
	curl -XDELETE "$(ES_URL)/map"

#look at settings of index "map"
get-map:
	curl -XGET "$(ES_URL)/map?pretty"


#get doc by index (put index there)
ind = 1
get1:
	curl -XGET "$(ES_URL)/map/_doc/$(ind)?pretty"

#match all with size
all:
	curl -XGET '$(ES_URL)/map/_search?scroll=10m&size=50&pretty' -H 'Content-Type: application/json' -d '{"query" : {"match_all" : {}}}'

#check my_analyzer on the text
check:
	curl -XGET "$(ES_URL)/map/_analyze?pretty" -H 'Content-Type: application/json' -d '{ "analyzer": "my_analyzer", "text": "администратора который" }'


# del docs by query
del:
	curl -XPOST "$(ES_URL)/map/_delete_by_query?pretty" -H 'Content-Type: application/json' -d'	{	"query": {		"match_all": {}		}	}	'
	curl -XDELETE "$(ES_URL)/map"

# see the space you have available on each node by running:
stats:
	curl -XGET $(ES_URL)/_nodes/stats/fs?pretty