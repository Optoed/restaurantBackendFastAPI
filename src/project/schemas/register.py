# src/project/schemas/register.py

from pydantic import BaseModel, ConfigDict


class RegisterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: str
    password: str
    role: str
