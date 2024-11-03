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
        query = "SELECT 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_recipes(
        self,
        session: AsyncSession,
    ) -> list[RecipeSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.recipe;"

        recipes = await session.execute(text(query))

        return [RecipeSchema.model_validate(dict(recipe)) for recipe in recipes.mappings().all()]

    async def get_recipe_by_id(
        self,
        session: AsyncSession,
        id_recipe: int
    ) -> RecipeSchema | None:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.recipe WHERE id = :id")

        result = await session.execute(query, {"id": id_recipe})

        recipe_row = result.mappings().first()

        if recipe_row:
            return RecipeSchema.model_validate(dict(recipe_row))
        return None

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

        recipe_row = result.mappings().first()

        if recipe_row:
            return RecipeSchema.model_validate(dict(recipe_row))
        return None

    async def update_recipe_by_id(
        self,
        session: AsyncSession,
        id_recipe: int,
        time_to_cook: datetime.time,
        name: str,
    ) -> RecipeSchema | None:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.recipe 
            SET time_to_cook = :time_to_cook, name = :name 
            WHERE id = :id 
            RETURNING id, time_to_cook, name
        """)

        result = await session.execute(query, {"id": id_recipe, "time_to_cook": time_to_cook, "name": name})

        updated_row = result.mappings().first()

        if updated_row:
            return RecipeSchema.model_validate(dict(updated_row))

        return None

    async def delete_recipe_by_id(
        self,
        session: AsyncSession,
        id_recipe: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.recipe WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_recipe})

        deleted_row = result.fetchone()

        return True if deleted_row else False