# src/project/infrastructure/postgres/repository/customer_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.infrastructure.postgres.models import Customer
from src.project.schemas.customer import CustomerSchema


class CustomerRepository:
    _collection: Type[Customer] = Customer

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_customers(
            self,
            session: AsyncSession
    ) -> list[CustomerSchema]:

        query = "SELECT * FROM customer;"
        result = await session.execute(text(query))

        return [
            CustomerSchema.model_validate(dict(customer))
            for customer in result.mappings().all()
        ]

    async def get_customer_by_id(
            self,
            session: AsyncSession,
            id_customer: int
    ) -> CustomerSchema | None:

        query = text("SELECT * FROM customer WHERE id = :id")
        result = await session.execute(query, {"id": id_customer})

        customer_row = result.mappings().first()

        if customer_row:
            return CustomerSchema.model_validate(dict(customer_row))

        return None

    async def insert_customer(
            self,
            session: AsyncSession,
            id: int,
            name: str,
            rating: float
    ) -> CustomerSchema | None:

        query = text("""
            INSERT INTO customer (name, rating) 
            VALUES (:name, :rating)
            RETURNING id, name, rating
        """)

        result = await session.execute(query, {
            "name": name,
            "rating": rating
        })

        customer_row = result.mappings().first()

        if customer_row:
            return CustomerSchema.model_validate(dict(customer_row))

        return None

    async def update_customer_by_id(
            self,
            session: AsyncSession,
            id_customer: int,
            name: str,
            rating: float
    ) -> CustomerSchema | None:

        query = text("""
            UPDATE customer 
            SET name = :name, rating = :rating
            WHERE id = :id 
            RETURNING id, rating
        """)

        result = await session.execute(query, {
            "id": id_customer,
            "name": name,
            "rating": rating
        })

        updated_row = result.mappings().first()

        if updated_row:
            return CustomerSchema.model_validate(dict(updated_row))

        return None

    async def delete_customer_by_id(
            self,
            session: AsyncSession,
            id_customer: int
    ) -> bool:

        query = text("DELETE FROM customer WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_customer})

        deleted_row = result.fetchone()

        return deleted_row is not None
