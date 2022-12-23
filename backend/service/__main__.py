import json

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from service.config import app
from service.endpoints.create_index_handler import api_router as create_routes
from service.endpoints.delete_handlers import api_router as delete_routes
from service.endpoints.get_handlers import api_router as get_routes

for route in (create_routes, get_routes, delete_routes):
    app.include_router(route)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def root(myBody: dict):
    key = list(dict(myBody).keys())[0]
    val = list(dict(myBody).values())[0]
    if key == "onload":
        return {
            "all": 1,
            "found": json.dumps(["all"]),
        }
    return {
        "search": "Hello World",
        "found": json.dumps([val]),
    }


# if __name__ == "__main__":
#     uvicorn.run("service.__main__:app", port=80, host="0.0.0.0", reload=True)
