from pydantic import BaseModel


class TextInput(BaseModel):
    id: int
    message: str


class TextOutput(BaseModel):
    id: str
    message: str
