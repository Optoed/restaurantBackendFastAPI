from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.project.schemas.user import UserSchema
from src.project.infrastructure.postgres.models import Users
from src.project.core.config import settings


class UsersRepository:
    _collection: Type[Users] = Users

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_users(
        self,
        session: AsyncSession,
    ) -> list[UserSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.users;"
        users = await session.execute(text(query))
        return [UserSchema.model_validate(dict(user)) for user in users.mappings().all()]

    async def get_user_by_id(
        self,
        session: AsyncSession,
        id_user: int
    ) -> UserSchema | None:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.users WHERE id = :id")
        result = await session.execute(query, {"id": id_user})
        user_row = result.mappings().first()

        if user_row:
            return UserSchema.model_validate(dict(user_row))
        return None

    async def insert_user(
        self,
        session: AsyncSession,
        name: str,
        email: str,
        password_hash: str,
        role: str  # Роль как строка
    ) -> UserSchema | None:
        query = text(f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.users (name, email, password_hash, role) 
            VALUES (:name, :email, :password_hash, :role)
            RETURNING id, name, email, role
        """)
        result = await session.execute(query, {"name": name, "email": email, "password_hash": password_hash, "role": role})

        user_row = result.mappings().first()

        if user_row:
            return UserSchema.model_validate(dict(user_row))
        return None

    async def update_user_by_id(
        self,
        session: AsyncSession,
        id_user: int,
        name: str,
        email: str,
        password_hash: str,
        role: str  # Роль как строка
    ) -> UserSchema | None:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.users 
            SET name = :name, email = :email, password_hash = :password_hash, role = :role 
            WHERE id = :id 
            RETURNING id, name, email, role
        """)
        result = await session.execute(query, {"id": id_user, "name": name, "email": email, "password_hash": password_hash, "role": role})
        updated_row = result.mappings().first()

        if updated_row:
            return UserSchema.model_validate(dict(updated_row))
        return None

    async def delete_user_by_id(
        self,
        session: AsyncSession,
        id_user: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.users WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_user})
        deleted_row = result.fetchone()

        return True if deleted_row else False
