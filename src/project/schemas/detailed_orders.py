import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional


class DetailedOrdersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_order: int
    id_customer: int
    customer_name: str
    dish_name: str
    dish_cost: int
    cook_name: str
    total_cost: int
    status: str
    order_date: datetime.datetime
