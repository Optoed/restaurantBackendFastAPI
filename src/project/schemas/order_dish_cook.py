# src/project/schemas/order_dish_cook.py

from pydantic import BaseModel, ConfigDict
from typing import Optional


class OrderDishCookSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_orders: int
    id_dish: int
    id_cook: Optional[int]
    status: str  # order_status
