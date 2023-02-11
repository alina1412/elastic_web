# elastic_web

Educational task:
- services:
    - fastapi backend: has endpoints to create, search in elasticsearch
    - elasticsearch in docker
    - web runs by nginx, simple html field for search


Current implementation has russian language mapping for elasticsearch.


To run locally:
- create env file
- `make build` (wait for containers to start)
- run `fill_index_from_csv.py` - it creates initial index and example data in elasticsearch
- work with http://localhost:8000/docs and web http://localhost:8080/

