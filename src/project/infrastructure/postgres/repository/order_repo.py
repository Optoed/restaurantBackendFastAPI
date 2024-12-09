# src/project/infrastructure/postgres/repository/order_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.infrastructure.postgres.models import Order
from src.project.schemas.order import OrderSchema


class OrderRepository:
    _collection: Type[Order] = Order

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_orders(
            self,
            session: AsyncSession
    ) -> list[OrderSchema]:

        query = "SELECT * FROM orders;"
        result = await session.execute(text(query))

        return [
            OrderSchema.model_validate(dict(order))
            for order in result.mappings().all()
        ]

    def get_orders_by_user_id(
            self,
            session: AsyncSession,
            id_user: int
    ) -> list[OrderSchema]:

        query = text("SELECT * FROM orders where ")

    async def get_order_by_id(
            self,
            session: AsyncSession,
            id_order: int
    ) -> OrderSchema | None:

        query = text("SELECT * FROM orders WHERE id = :id")
        result = await session.execute(query, {"id": id_order})

        order_row = result.mappings().first()

        if order_row:
            return OrderSchema.model_validate(dict(order_row))

        return None

    async def insert_order(
            self,
            session: AsyncSession,
            id: int,
            id_waiter: int,
            id_customer: int,
            total_cost: int,
            status: str
    ) -> OrderSchema | None:

        query = text("""
            INSERT INTO orders (id_waiter, id_customer, total_cost, status) 
            VALUES (:id_waiter, :id_customer, :total_cost, :status)
            RETURNING id, id_waiter, id_customer, total_cost, status
        """)

        result = await session.execute(query, {
            "id_waiter": id_waiter,
            "id_customer": id_customer,
            "total_cost": total_cost,
            "status": status
        })

        order_row = result.mappings().first()

        if order_row:
            return OrderSchema.model_validate(dict(order_row))

        return None

    async def update_order_by_id(
            self,
            session: AsyncSession,
            id_order: int,
            id_waiter: int,
            id_customer: int,
            total_cost: int,
            status: str
    ) -> OrderSchema | None:

        query = text("""
            UPDATE orders 
            SET id_waiter = :id_waiter, id_customer = :id_customer, 
                total_cost = :total_cost, status = :status 
            WHERE id = :id 
            RETURNING id, id_waiter, id_customer, total_cost, status
        """)

        result = await session.execute(query, {
            "id": id_order,
            "id_waiter": id_waiter,
            "id_customer": id_customer,
            "total_cost": total_cost,
            "status": status
        })

        updated_row = result.mappings().first()

        if updated_row:
            return OrderSchema.model_validate(dict(updated_row))

        return None

    async def delete_order_by_id(
            self,
            session: AsyncSession,
            id_order: int
    ) -> bool:

        query = text("DELETE FROM orders WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_order})

        deleted_row = result.fetchone()

        return deleted_row is not None

