import datetime

from pydantic import BaseModel, ConfigDict


class RecipeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    time_to_cook: datetime.time
    name: str

