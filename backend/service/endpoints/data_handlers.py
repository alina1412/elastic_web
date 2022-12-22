
from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Query, status
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from elasticsearch.exceptions import NotFoundError

from service.utils.errors import NotInElastic  # isort: skip
from service.utils.elastic_logic import (
    elastic_insert
)  # isort: skip

api_router = APIRouter(
    prefix="/v1",
    tags=["data"],
)



@api_router.put(
    "/add-data",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "No index"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def create_data_handler(request: Request, 
    index_name: str = Query(default="", min_length=1, description="index name"),
    doc_id: str = Query(default="", min_length=1, description="doc id"),
    message: str = Query(default="", min_length=1, description="message"),

    ):
    """"""
    if not index_name.strip() or not message.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="nothing to create")

    elastic_client: AsyncElasticsearch = request.app.state.elastic_client
    if not elastic_client.indices.exists(index=index_name):
        raise HTTPException(404, detail="no index")
    
    await elastic_insert(index_name, {"id": doc_id, "message": message})