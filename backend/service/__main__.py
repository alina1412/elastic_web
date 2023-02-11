import json

import uvicorn
from fastapi import HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

# fmt: off
from service.config import ElasticConfig, app # isort: skip
from service.endpoints.create_index_handler import api_router as create_routes # isort: skip
from service.endpoints.data_handlers import api_router as create_data # isort: skip
from service.endpoints.delete_handlers import api_router as delete_routes # isort: skip
from service.endpoints.get_handlers import api_router as get_routes # isort: skip
from service.utils.elastic_logic import get_all_from_index, get_matching_by_message # isort: skip
from service.utils.formatters import prepare_results # isort: skip
from service.utils.errors import NoIndex  # isort: skip
# fmt: on


for route in (create_routes, get_routes, delete_routes, create_data):
    app.include_router(route)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_onload_data_from_index(index):
    res = await get_all_from_index(index)
    res = prepare_results(res)
    print(res)
    return json.dumps(
        {
            "all": 1,
            "found": json.dumps(res),
        }
    )


async def get_searching_data_from_index(val, request, index):
    params = {
        "query": val,
        "size": ElasticConfig.elastic_size,
        "index_name": index,
    }
    res = await get_matching_by_message(params, request)
    res = prepare_results(res)
    print(res)
    if not res:
        res = [{"message": "not found"}]
    return {
        "search": "Hello World",
        "found": json.dumps(res),
    }


async def get_data_to_show(key, val, request, index):
    if key == "onload":
        return await get_onload_data_from_index(index)
    else:
        return await get_searching_data_from_index(val, request, index)


@app.post("/")
async def root(request: Request, myBody: dict):
    try:
        key = list(dict(myBody).keys())[0]
        val = list(dict(myBody).values())[0]
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST) from exc

    index_default = ElasticConfig.elastic_index
    try:
        data = await get_data_to_show(key, val, request, index_default)
        return data
    except NoIndex:
        raise HTTPException(404, detail="no index")
    except Exception as exc:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) from exc


# if __name__ == "__main__":
#     uvicorn.run("service.__main__:app", port=80, host="0.0.0.0", reload=True)
