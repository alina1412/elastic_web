import uuid

from elasticsearch import AsyncElasticsearch, NotFoundError
from starlette.requests import Request

from service.config import app  # isort: skip
from service.mapping import elastic_text_settings, mapping_for_index  # isort: skip
from service.utils.errors import NoIndex, NotInElastic  # isort: skip


async def doc_delete_from_index(index_name, doc_id) -> None:
    """Deletes doc from index in elastic by id
    id - manual from schema (should be unique)
    """
    elastic_client = app.state.elastic_client
    if not elastic_client.indices.exists(index=index_name):
        raise NoIndex
    try:
        elastic_client.delete(index=index_name, id=doc_id)
    except NotFoundError:
        raise NotInElastic


async def get_matching_by_message(params, request) -> dict:
    searching = {
        "size": params["size"],
        "query": {"match": {"message": {"operator": "or", "query": params["query"]}}},
        "rescore": {
            "window_size": params["size"],
            "query": {
                "rescore_query": {
                    "match_phrase": {"message": {"query": params["query"], "slop": 2}}
                },
                "query_weight": 0.7,
                "rescore_query_weight": 1.2,
            },
        },
    }
    print("get_matching_by_message")
    elastic_client: AsyncElasticsearch = request.app.state.elastic_client
    if not elastic_client.indices.exists(index=params["index_name"]):
        raise NoIndex
    try:
        res = elastic_client.search(index=params["index_name"], body=searching)
        return dict(res)
    except Exception as exc:
        raise exc


async def create_elastic_index(name) -> None:
    """Creates index in elastic by name"""
    try:
        elastic_client: AsyncElasticsearch = app.state.elastic_client
        elastic_client.indices.create(
            index=name,
            mappings=mapping_for_index,
            settings=elastic_text_settings,
        )
    except Exception as exc:
        raise exc


async def elastic_insert(index_name: str, insert_data: dict, id=None) -> None:
    """Insert data into elastic index"""
    id = id or uuid.uuid4()
    app.state.elastic_client.index(index=index_name, id=id, document=insert_data)


async def delete_index(request: Request, index_name: str) -> None:
    """Delete index from elastic"""
    elastic_client: AsyncElasticsearch = request.app.state.elastic_client
    try:
        elastic_client.indices.delete(index=index_name)
    except NotFoundError as exc:
        raise exc


async def get_all_from_index(index_name) -> dict:
    searching = {"query": {"match_all": {}}}
    elastic_client: AsyncElasticsearch = app.state.elastic_client
    if not elastic_client.indices.exists(index=index_name):
        raise NoIndex
    res = elastic_client.search(index=index_name, body=searching)
    return dict(res)
