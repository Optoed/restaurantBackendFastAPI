# src/project/schemas/login.py

from pydantic import BaseModel, ConfigDict


class LoginSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    password: str
