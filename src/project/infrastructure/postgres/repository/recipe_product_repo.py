from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.schemas.recipe_product import RecipeProductSchema
from src.project.infrastructure.postgres.models import RecipeProduct
from src.project.core.config import settings


class RecipeProductRepository:
    _collection: Type[RecipeProduct] = RecipeProduct

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "SELECT 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_recipe_products(
        self,
        session: AsyncSession,
    ) -> list[RecipeProductSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.recipe_product;"

        recipe_products = await session.execute(text(query))

        return [RecipeProductSchema.model_validate(dict(recipe_product)) for recipe_product in recipe_products.mappings().all()]

    async def get_recipe_product_by_id(
            self,
            session: AsyncSession,
            id_recipe: int,
            id_product: int
    ) -> RecipeProductSchema | None:
        query = text(f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.recipe_product 
            WHERE id_recipe = :id_recipe AND id_product = :id_product
        """)

        result = await session.execute(query, {"id_recipe": id_recipe, "id_product": id_product})

        recipe_product_row = result.mappings().first()

        if recipe_product_row:
            return RecipeProductSchema.model_validate(dict(recipe_product_row))
        return None

    async def insert_recipe_product(
            self,
            session: AsyncSession,
            id_recipe: int,
            id_product: int
    ) -> RecipeProductSchema | None:
        query = text(f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.recipe_product (id_recipe, id_product) 
            VALUES (:id_recipe, :id_product)
            RETURNING id_recipe, id_product
        """)
        result = await session.execute(query, {"id_recipe": id_recipe, "id_product": id_product})

        recipe_product_row = result.mappings().first()

        if recipe_product_row:
            return RecipeProductSchema.model_validate(dict(recipe_product_row))
        return None

    async def delete_recipe_product_by_id(
            self,
            session: AsyncSession,
            id_recipe: int,
            id_product: int
    ) -> bool:
        query = text(f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.recipe_product 
            WHERE id_recipe = :id_recipe AND id_product = :id_product 
            RETURNING id_recipe, id_product
        """)

        result = await session.execute(query, {"id_recipe": id_recipe, "id_product": id_product})

        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_recipe_product_by_id(
            self,
            session: AsyncSession,
            id_recipe: int,
            id_product: int
    ) -> RecipeProductSchema | None:
        # В данном случае обновление может быть неуместным, так как это связь
        # Но если вы хотите обновить, например, id_product, можно сделать так:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.recipe_product 
            SET id_product = :new_id_product 
            WHERE id_recipe = :id_recipe AND id_product = :id_product 
            RETURNING id_recipe, id_product
        """)

        result = await session.execute(query, {"id_recipe": id_recipe, "id_product": id_product, "new_id_product": new_id_product})

        updated_row = result.mappings().first()

        if updated_row:
            return RecipeProductSchema.model_validate(dict(updated_row))

        return None


