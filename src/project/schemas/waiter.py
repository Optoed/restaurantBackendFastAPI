# src/project/schemas/waiter.py

from pydantic import BaseModel, ConfigDict
from typing import Optional


class WaiterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    salary: int
    rating: Optional[float]
    status: str  # worker_status
