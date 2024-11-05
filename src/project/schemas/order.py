# src/project/schemas/order.py

from pydantic import BaseModel, ConfigDict


class OrderSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_waiter: int
    id_customer: int
    total_cost: int
    status: str  # Используйте str для статуса, можно добавить валидацию
