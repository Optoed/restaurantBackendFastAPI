from typing import Type

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.infrastructure.security.bcrypt import hash_password, verify_password
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

    async def get_user_by_email(
        self,
        session: AsyncSession,
        email: str
    ) -> UserSchema | None:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.users WHERE email = :email")
        result = await session.execute(query, {"email": email})
        user_row = result.mappings().first()

        if user_row:
            return UserSchema.model_validate(dict(user_row))
        return None

    async def register_user(
        self,
        session: AsyncSession,
        name: str,
        email: str,
        password: str,  # помним что при регистрации пользователь указывает обычный (не хэшированный) пароль
        role: str  # Роль как строка, пока что допустим 'admin' и 'user'
    ) -> UserSchema | None:

        # TODO: убери потом этот костыль с проверкой на role
        if role not in ["user", "admin"]:
            raise HTTPException(status_code=400, detail="Invalid role")

        query = text(f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.users (name, email, password_hash, role) 
            VALUES (:name, :email, :password_hash, :role)
            RETURNING id, name, email, password_hash, role
        """)

        # пользователь указывает password, мы его хэшируем и кладем в бд password_hash
        password_hash = hash_password(password)

        # TODO: "либо делаем enum - это чуть сложнее, но гораздо лучше"
        result = await session.execute(query, {"name": name,
                                               "email": email,
                                               "password_hash": password_hash,
                                               "role": role})
        user_row = result.mappings().first()

        if user_row:
            return UserSchema.model_validate(dict(user_row))
        return None

    # TODO: допиши логику auth_user, где выдается JWT-token
    # TODO: также мы указываем еще и пароль который сранивается с хэшированным: ДОБАВЬ ПОЛЕ password

    async def login_user(
        self,
        session: AsyncSession,
        email: str,
        password: str
    ) -> UserSchema | None:
        user = await self.get_user_by_email(session=session, email=email)
        if not user:
            raise HTTPException(status_code=404, detail="User with such email not found")

        print(password, " ", user.password_hash)

        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid password")

        #TODO: нужно создать, вернуть токен и добавить его в бд
        # token = seft.create_jwt_token(user.id, user.role)
        # return {"user": user, "token": token}

        return user

    async def delete_user_by_id(
        self,
        session: AsyncSession,
        id_user: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.users WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_user})
        deleted_row = result.fetchone()

        return True if deleted_row else False
