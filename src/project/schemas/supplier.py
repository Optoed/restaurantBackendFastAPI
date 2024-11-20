
from pydantic import BaseModel, ConfigDict


class SupplierSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    cost: int
    rating: float

