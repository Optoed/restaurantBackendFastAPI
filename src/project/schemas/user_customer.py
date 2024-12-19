import datetime

from pydantic import BaseModel, ConfigDict


class UserCustomerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_user: int
    id_customer: int

