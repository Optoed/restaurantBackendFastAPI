# src/project/infrastructure/postgres/repository/cook_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.infrastructure.postgres.models import Cook
from src.project.schemas.cook import CookSchema


class CookRepository:
    _collection: Type[Cook] = Cook

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False


    async def get_all_cooks(
            self,
            session: AsyncSession
    ) -> list[CookSchema]:
        query = "SELECT * FROM cook;"
        result = await session.execute(text(query))

        return [
            CookSchema.model_validate(dict(cook))
            for cook in result.mappings().all()
        ]

    async def get_cook_by_id(
            self,
            session: AsyncSession,
            id_cook: int
    ) -> CookSchema | None:
        query = text("SELECT * FROM cook WHERE id = :id")
        result = await session.execute(query, {"id": id_cook})

        cook_row = result.mappings().first()

        if cook_row:
            return CookSchema.model_validate(dict(cook_row))

        return None

    async def insert_cook(
            self,
            session: AsyncSession,
            id: int,
            name: str,
            post: str,
            salary: int,
            rating: float,
            status: str
    ) -> CookSchema | None:
        query = text("""
            INSERT INTO cook (name, post, salary, rating, status) 
                        VALUES (:name, :post, :salary, :rating, :status)
            RETURNING id, name, post, salary, rating, status
        """)

        result = await session.execute(query, {
            "name": name,
            "post": post,
            "salary": salary,
            "rating": rating,
            "status": status
        })

        cook_row = result.mappings().first()

        if cook_row:
            return CookSchema.model_validate(dict(cook_row))

        return None

    async def update_cook_by_id(
        self,
        session: AsyncSession,
        id_cook: int,
        name: str,
        post: str,
        salary: int,
        rating: float,
        status: str
    ) -> CookSchema | None:

        query = text("""
            UPDATE cook 
            SET name = :name, post = :post, salary = :salary, 
                rating = :rating, status = :status 
            WHERE id = :id 
            RETURNING id, name, post, salary, rating, status
        """)

        result = await session.execute(query, {
            "id": id_cook,
            "name": name,
            "post": post,
            "salary": salary,
            "rating": rating,
            "status": status
        })

        updated_row = result.mappings().first()

        if updated_row:
            return CookSchema.model_validate(dict(updated_row))

        return None

    async def delete_cook_by_id(
        self,
        session: AsyncSession,
        id_cook: int
    ) -> bool:

        query = text("DELETE FROM cook WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_cook})

        deleted_row = result.fetchone()

        return deleted_row is not None
