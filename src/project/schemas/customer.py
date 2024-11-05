# src/project/schemas/customer.py

from pydantic import BaseModel, ConfigDict
from typing import Optional


class CustomerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: Optional[str]
    rating: Optional[float]
