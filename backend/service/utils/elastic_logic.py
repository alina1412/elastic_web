from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError

from service.config import app  # isort: skip
from service.mapping import elastic_text_settings, mapping_for_index  # isort: skip
from service.utils.errors import NoIndex, NotInElastic  # isort: skip


async def doc_delete_from_index(index_name, doc_id) -> None:
    """deletes doc from index in elastic by id
    id - manual from schema (should be unique)"""
    query = {"query": {"term": {"id": id}}}
    print("doc_delete_from_index")
    return
    # res = app.state.elastic_client.search(index=index_name, body=query)
    # id = res.get("hits", {}).get("hits", [{}])[0].get("_source", {}).get("id")
    # hits = res.get("hits", {}).get("hits", [{}])
    # if not hits:
    #     raise NotInElastic
    # inner_id = hits[0].get("_id")
    # if not inner_id:
    #     raise NotInElastic
    # app.state.elastic_client.delete(index=index_name, id=inner_id)


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
    return {}
    # try:
    #     elastic_client: AsyncElasticsearch = request.app.state.elastic_client
    #     res = elastic_client.search(index=params["index_name"], body=searching)
    #     return dict(res)
    # except NotFoundError:
    #     raise NoIndex


async def create_elastic_index(name) -> None:
    """creates index in elastic by name"""
    try:
        elastic_client: AsyncElasticsearch = app.state.elastic_client
        elastic_client.indices.create(
            index=name,
            mappings=mapping_for_index,
            settings=elastic_text_settings,
        )
    except Exception as exc:
        raise exc


async def elastic_insert(index_name: str, insert_data: dict) -> None:
    """insert data into elastic index"""
    app.state.elastic_client.index(index=index_name, document=insert_data)
