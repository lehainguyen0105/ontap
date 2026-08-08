from pydantic import BaseModel, ConfigDict
from typing import Optional

class AuthorBaseSchema(BaseModel):
    name: str
    email: str
    bio: Optional[str] = None

class AuthorResponseSchema(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)