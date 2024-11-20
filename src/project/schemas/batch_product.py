import datetime

from pydantic import BaseModel, ConfigDict


class BatchProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_batch: int
    id_product: int
    amount: int
    expiration_date: datetime.date

