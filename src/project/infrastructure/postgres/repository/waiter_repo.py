# src/project/infrastructure/postgres/repository/waiter_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.infrastructure.postgres.models import Waiter
from src.project.schemas.waiter import WaiterSchema


class WaiterRepository:
    _collection: Type[Waiter] = Waiter

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_waiters(
            self,
            session: AsyncSession
    ) -> list[WaiterSchema]:

        query = "SELECT * FROM waiter;"
        result = await session.execute(text(query))

        return [
            WaiterSchema.model_validate(dict(waiter))
            for waiter in result.mappings().all()
        ]

    async def get_waiter_by_id(
            self,
            session: AsyncSession,
            id_waiter: int
    ) -> WaiterSchema | None:

        query = text("SELECT * FROM waiter WHERE id = :id")
        result = await session.execute(query, {"id": id_waiter})

        waiter_row = result.mappings().first()

        if waiter_row:
            return WaiterSchema.model_validate(dict(waiter_row))

        return None

    async def insert_waiter(
            self,
            session: AsyncSession,
            id: int,
            name: str,
            salary: int,
            rating: float,
            status: str
    ) -> WaiterSchema | None:

        query = text("""
            INSERT INTO waiter (name, salary, rating, status) 
            VALUES (:name, :salary, :rating, :status)
            RETURNING id, name, salary, rating, status
        """)

        result = await session.execute(query, {
            "name": name,
            "salary": salary,
            "rating": rating,
            "status": status
        })

        waiter_row = result.mappings().first()

        if waiter_row:
            return WaiterSchema.model_validate(dict(waiter_row))

        return None

    async def update_waiter_by_id(
            self,
            session: AsyncSession,
            id_waiter: int,
            name: str,
            salary: int,
            rating: float,
            status: str
    ) -> WaiterSchema | None:

        query = text("""
            UPDATE waiter 
            SET name = :name, salary = :salary, rating = :rating, status = :status 
            WHERE id = :id 
            RETURNING id, name, salary, rating, status
        """)

        result = await session.execute(query, {
            "id": id_waiter,
            "name": name,
            "salary": salary,
            "rating": rating,
            "status": status
        })

        updated_row = result.mappings().first()

        if updated_row:
            return WaiterSchema.model_validate(dict(updated_row))

        return None

    async def delete_waiter_by_id(
            self,
            session: AsyncSession,
            id_waiter: int
    ) -> bool:

        query = text("DELETE FROM waiter WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_waiter})

        deleted_row = result.fetchone()

        return deleted_row is not None
