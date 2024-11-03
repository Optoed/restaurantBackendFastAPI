import datetime
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.schemas.recipe import RecipeSchema
from src.project.infrastructure.postgres.models import Recipe

from src.project.core.config import settings


class RecipeRepository:
    _collection: Type[Recipe] = Recipe

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_recipes(
        self,
        session: AsyncSession,
    ) -> list[RecipeSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.recipe;"

        recipes = await session.execute(text(query))

        return [RecipeSchema.model_validate(dict(recipe)) for recipe in recipes.mappings().all()]

    async def insert_recipe(
            self,
            session: AsyncSession,
            time_to_cook: datetime.time,
            name: str,
    ) -> RecipeSchema | None:
        query = text(f"""
                       INSERT INTO {settings.POSTGRES_SCHEMA}.recipe (time_to_cook, name) 
                       VALUES (:time_to_cook, :name)
                       RETURNING id, time_to_cook, name
                   """)
        result = await session.execute(query, {"time_to_cook": time_to_cook, "name": name})

        product_row = result.mappings().first()

        if product_row:
            return RecipeSchema.model_validate(dict(product_row))
        return None
