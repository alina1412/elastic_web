import elasticsearch
from fastapi import APIRouter, Query, status
from fastapi.exceptions import HTTPException
from starlette.requests import Request

from service.utils.elastic_logic import create_elastic_index  # isort: skip
from service.utils.errors import NoIndex  # isort: skip
from service.config import econf  # isort: skip


api_router = APIRouter(
    prefix="/v1",
    tags=["index"],
)


@api_router.get(
    "/create-index",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
    },
)
async def create_index_handler(
    request: Request,
    name: str = Query(default="", min_length=1, description="index name"),
):
    """create index"""
    if not name.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="nothing to create")

    try:
        await create_elastic_index(name)
    except elasticsearch.exceptions.RequestError as exc:
        if exc.error == "resource_already_exists_exception":
            print("Index already exists")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Index already exists") from exc
        raise exc
