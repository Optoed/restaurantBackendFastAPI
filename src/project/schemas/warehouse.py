
from pydantic import BaseModel, ConfigDict


class WarehouseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    location: str
    how_full: float

