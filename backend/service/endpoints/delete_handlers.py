from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from service.utils.logic import doc_delete_from_index

from backend.service.utils.errors import NotInElastic

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
    doc_id: int,
    index_name: str = "map",
):
    """Deletes a document from elastic index by id"""

    try:
        await doc_delete_from_index(index_name, doc_id)
    except NotInElastic as exc:
        raise HTTPException(404, detail="nothing to delete") from exc
    except Exception as exc:
        print(exc)
        raise HTTPException(503, detail="some error during deletion") from exc
