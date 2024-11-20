
from pydantic import BaseModel, ConfigDict


class UsersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: str
    password_hash: str

