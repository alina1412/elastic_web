from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import APIRouter, Query, status
from fastapi.exceptions import HTTPException
from starlette.requests import Request

# fmt: off
from service.utils.elastic_logic import elastic_insert  # isort: skip
from service.utils.errors import NotInElastic  # isort: skip
# fmt: on

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
async def create_data_handler(
    request: Request,
    index_name: str = Query(default="", min_length=1, description="index name"),
    doc_id: str = Query(default="", min_length=1, description="doc id"),
    message: str = Query(default="", min_length=1, description="message"),
):
    """"""
    index_name = index_name.strip()
    message = message.strip()
    doc_id = doc_id.strip()
    if not index_name or not message:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="nothing to create")

    elastic_client: AsyncElasticsearch = request.app.state.elastic_client
    if not elastic_client.indices.exists(index=index_name):
        raise HTTPException(404, detail="no index")

    await elastic_insert(index_name, {"message": message}, doc_id)
