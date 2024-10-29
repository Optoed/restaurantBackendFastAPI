from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.user import UserSchema
from project.infrastructure.postgres.models import User

from project.core.config import settings


class UserRepository:
    _collection: Type[User] = User

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_users(
        self,
        session: AsyncSession,
    ) -> list[UserSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.users;"

        users = await session.execute(text(query))

        return [UserSchema.model_validate(obj=user) for user in users.mappings().all()]

