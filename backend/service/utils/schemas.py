from pydantic import BaseModel


class TextInput(BaseModel):
    id: int
    message: str
