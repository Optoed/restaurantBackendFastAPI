# src/project/infrastructure/postgres/repository/dish_repo.py

import datetime
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.project.schemas.dish import DishSchema
from src.project.infrastructure.postgres.models import Dish
from src.project.core.config import settings

class DishRepository:
    _collection: Type[Dish] = Dish

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_dishes(self, session: AsyncSession) -> list[DishSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.dish;"
        dishes = await session.execute(text(query))
        return [DishSchema.model_validate(dict(dish)) for dish in dishes.mappings().all()]

    async def get_dish_by_id(self, session: AsyncSession, id_dish: int) -> DishSchema | None:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.dish WHERE id = :id")
        result = await session.execute(query, {"id": id_dish})
        dish_row = result.mappings().first()
        if dish_row:
            return DishSchema.model_validate(dict(dish_row))
        return None

    async def insert_dish(
            self,
            session: AsyncSession,
            id_recipe: int,
            name: str,
            cost: int,
            rating: float | None
    ) -> DishSchema | None:
        query = text(f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.dish (id_recipe, name, cost, rating) 
            VALUES (:id_recipe, :name, :cost, :rating)
            RETURNING id, id_recipe, name, cost, rating
        """)
        result = await session.execute(query, {"id_recipe": id_recipe, "name": name, "cost": cost, "rating": rating})
        dish_row = result.mappings().first()
        if dish_row:
            return DishSchema.model_validate(dict(dish_row))
        return None

    async def update_dish_by_id(self, session: AsyncSession, id_dish: int, id_recipe: int, name: str, cost: int, rating: float | None) -> DishSchema | None:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.dish 
            SET id_recipe = :id_recipe, name = :name, cost = :cost, rating = :rating 
            WHERE id = :id 
            RETURNING id, id_recipe, name, cost, rating
            """)
        result = await session.execute(query, {
            "id": id_dish,
            "id_recipe": id_recipe,
            "name": name,
            "cost": cost,
            "rating": rating
        })
        updated_row = result.mappings().first()
        if updated_row:
            return DishSchema.model_validate(dict(updated_row))
        return None

    async def delete_dish_by_id(self, session: AsyncSession, id_dish: int) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.dish WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_dish})
        deleted_row = result.fetchone()
        return True if deleted_row else False
