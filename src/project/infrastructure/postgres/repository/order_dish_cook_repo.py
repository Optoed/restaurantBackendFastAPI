# src/project/infrastructure/postgres/repository/order_dish_cook_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.infrastructure.postgres.models import OrdersDishCook
from src.project.schemas.order_dish_cook import OrderDishCookSchema


class OrderDishCookRepository:
    _collection: Type[OrdersDishCook] = OrdersDishCook

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_entries(
            self,
            session: AsyncSession
    ) -> list[OrderDishCookSchema]:

        query = "SELECT * FROM order_dish_cook;"
        result = await session.execute(text(query))

        return [
            OrderDishCookSchema.model_validate(dict(entry))
            for entry in result.mappings().all()
        ]

    async def get_entry_by_id(
            self,
            session: AsyncSession,
            id_entry: int
    ) -> OrderDishCookSchema | None:

        query = text("SELECT * FROM order_dish_cook WHERE id = :id")
        result = await session.execute(query, {"id": id_entry})

        entry_row = result.mappings().first()

        if entry_row:
            return OrderDishCookSchema.model_validate(dict(entry_row))

        return None

    async def insert_entry(
            self,
            session: AsyncSession,
            id: int,
            id_orders: int,
            id_dish: int,
            id_cook: int,
            status: str
    ) -> OrderDishCookSchema | None:

        query = text("""
            INSERT INTO order_dish_cook (id_orders, id_dish, id_cook, status) 
            VALUES (:id_orders, :id_dish, :id_cook, :status)
            RETURNING id, id_orders, id_dish, id_cook, status
        """)

        result = await session.execute(query, {
            "id_orders": id_orders,
            "id_dish": id_dish,
            "id_cook": id_cook,
            "status": status
        })

        entry_row = result.mappings().first()

        if entry_row:
            return OrderDishCookSchema.model_validate(dict(entry_row))

        return None

    async def delete_entry_by_id(
            self,
            session: AsyncSession,
            id_entry: int
    ) -> bool:

        query = text("DELETE FROM order_dish_cook WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_entry})

        deleted_row = result.fetchone()

        return deleted_row is not None
