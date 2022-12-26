from fastapi import APIRouter, Query, status
from fastapi.exceptions import HTTPException
from starlette.requests import Request


from service.config import econf  # isort: skip
from service.utils.errors import NoIndex  # isort: skip
from service.utils.elastic_logic import get_matching_by_message  # isort: skip
from service.utils.formatters import prepare_results  # isort: skip
from service.utils.schemas import TextInput # isort: skip

api_router = APIRouter(
    prefix="/v1",
    tags=["search"],
)


@api_router.get(
    "/match-data",
    status_code=status.HTTP_200_OK,
    response_model=list[TextInput],
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "some error"},
    },
)
async def get_matching_handler(
    request: Request,
    index_name: str = Query(default="map", min_length=1, description="index name"),
    query: str = Query(default="", min_length=2, description="search query"),
):
    """gets matching docs from elastic by query,"""
    if not query.strip() or not index_name.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="nothing to search")

    params = {
        "query": query,
        "size": econf.elastic_size,
        "index_name": index_name,
    }
    try:
        res = await get_matching_by_message(params, request)
        res = prepare_results(res)
        return res
    except NoIndex as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, f"No such index '{index_name}' to search"
        ) from exc
