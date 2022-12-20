import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def root(myBody: dict):
    return {"message": "Hello World", "m2": "TODO"}


# if __name__ == "__main__":
#     uvicorn.run("service.__main__:app", port=80, host="0.0.0.0", reload=True)
