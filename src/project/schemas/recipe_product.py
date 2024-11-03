from pydantic import BaseModel, ConfigDict


class RecipeProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_recipe: int
    id_product: int
