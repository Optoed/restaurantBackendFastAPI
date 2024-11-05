# src/project/schemas/cook.py

from pydantic import BaseModel, ConfigDict
from typing import Optional


class CookSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    post: Optional[str]
    salary: Optional[int]
    rating: Optional[float]
    status: str  # worker_status
