
from pydantic import BaseModel, ConfigDict


class BatchSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_supplier: int
    id_warehouse: int
    total_cost: int

