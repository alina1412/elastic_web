import json

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

# fmt: off
from service.config import ElasticConfig, app
from service.endpoints.create_index_handler import api_router as create_routes
from service.endpoints.delete_handlers import api_router as delete_routes
from service.endpoints.get_handlers import api_router as get_routes
from service.utils.elastic_logic import get_all_from_index, get_matching_by_message
from service.utils.formatters import prepare_results

# fmt: on


for route in (create_routes, get_routes, delete_routes):
    app.include_router(route)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def root(request: Request, myBody: dict):
    key = list(dict(myBody).keys())[0]
    val = list(dict(myBody).values())[0]
    index_default = ElasticConfig.elastic_index

    if key == "onload":
        res = await get_all_from_index(index_default)
        res = prepare_results(res)
        print(res)
        return json.dumps({
            "all": 1,
            "found": json.dumps(res),
        })

    params = {
        "query": val,
        "size": ElasticConfig.elastic_size,
        "index_name": index_default,
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


# if __name__ == "__main__":
#     uvicorn.run("service.__main__:app", port=80, host="0.0.0.0", reload=True)
