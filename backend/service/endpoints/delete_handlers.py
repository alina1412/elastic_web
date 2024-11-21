from elasticsearch.exceptions import NotFoundError
from fastapi import APIRouter, Query, status
from fastapi.exceptions import HTTPException
from starlette.requests import Request

# fmt: off
from service.utils.errors import NotInElastic  # isort: skip # noqa 
from service.utils.elastic_logic import delete_index, doc_delete_from_index  # isort: skip # noqa
# fmt: on

api_router = APIRouter(
    prefix="/v1",
    tags=["delete"],
)


@api_router.delete(
    "/delete-data",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_404_NOT_FOUND: {"description": "Nothing to delete"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "some error during deletion"
        },
    },
)
async def delete_one_handler(
    doc_id: str,
    index_name: str = Query(default="map", min_length=1, description="index name"),
):
    """Deletes a document from elastic index by id"""

    try:
        await doc_delete_from_index(index_name, doc_id)
    except NotInElastic as exc:
        raise HTTPException(404, detail="nothing to delete") from exc
    except Exception as exc:
        print(exc)
        raise HTTPException(503, detail="some error during deletion") from exc


@api_router.delete(
    "/delete-index",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_404_NOT_FOUND: {"description": "No index to delete"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def delete_index_handler(
    request: Request,
    index_name: str = Query(default="map", min_length=1, description="index name"),
):
    """Delete_index from elastic"""
    try:
        await delete_index(request, index_name)
    except NotFoundError as exc:
        raise HTTPException(404, detail="No index to delete") from exc
