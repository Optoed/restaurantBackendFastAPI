# src/project/schemas/dish.py

from pydantic import BaseModel, ConfigDict


class DishSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_recipe: int
    name: str
    cost: int
    rating: float | None  # Рейтинг может быть None
