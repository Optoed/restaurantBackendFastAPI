import logging
from typing import Type

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from sqlalchemy.testing.pickleable import User

from src.project.infrastructure.security.JWT_token import create_access_token
from src.project.infrastructure.security.bcrypt import hash_password, verify_password
from src.project.schemas.customer import CustomerSchema
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

    from sqlalchemy.future import select
    from sqlalchemy.exc import IntegrityError

    async def register_user(
            self,
            session: AsyncSession,
            name: str,
            email: str,
            password: str,  # обычный (не хэшированный) пароль
            role: str  # Роль как строка, пока что допустим 'admin' и 'user'
    ) -> UserSchema | None:

        # TODO: убери потом этот костыль с проверкой на role
        if role not in ["user", "admin"]:
            raise HTTPException(status_code=400, detail="Invalid role")

        # Check if the user already exists
        query = text(f"SELECT 1 FROM {settings.POSTGRES_SCHEMA}.users WHERE email = :email LIMIT 1")
        result = await session.execute(query, {"email": email})
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        # If user does not exist, insert the new user
        password_hash = hash_password(password)

        query = text(f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.users (name, email, password_hash, role) 
            VALUES (:name, :email, :password_hash, :role)
            RETURNING id, name, email, password_hash, role
        """)

        query_customer = text(f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.customer (name, rating)
            VALUES (:name, :rating)
            RETURNING id, name, rating
        """)

        query_relate_user_and_customer = text(f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.user_customer (id_user, id_customer)
            VALUES (:id_user, :id_customer)
            RETURNING id_user, id_customer
        """)

        try:
            result = await session.execute(query, {"name": name,
                                                   "email": email,
                                                   "password_hash": password_hash,
                                                   "role": role})
            user_row = result.mappings().first()

            print("user_row", user_row)

            result_customer = await session.execute(query_customer, {"name": name,
                                                                     "rating": 0.0})

            customer_row = result_customer.mappings().first()

            print("customer_row", customer_row)

            if not customer_row:
                raise HTTPException(status_code=500, detail="Error while creating new customer")

            user = UserSchema.model_validate(dict(user_row))
            customer = CustomerSchema.model_validate(dict(customer_row))

            id_user = user.id
            id_customer = customer.id

            print("id:", id_user, id_customer)

            result_relate_user_and_customer = await session.execute(query_relate_user_and_customer,
                                                                    {"id_user": id_user,
                                                                     "id_customer": id_customer})

            print("relate", result_relate_user_and_customer)

            if not result_relate_user_and_customer.mappings().first():
                raise HTTPException(status_code=500, detail="Error while creating new relate user_customer")

            if user_row:
                return UserSchema.model_validate(dict(user_row))

            return None

        except IntegrityError:
            raise HTTPException(status_code=400, detail="Error while registering the user")

    async def login_user(
        self,
        session: AsyncSession,
        email: str,
        password: str
    ) -> dict:
        user = await self.get_user_by_email(session=session, email=email)
        if not user:
            raise HTTPException(status_code=404, detail="User with such email not found")

        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid password")

        token = create_access_token({"user_id": user.id, "role": user.role})

        query_get_id_customer = text(f"""
                    SELECT id_customer FROM {settings.POSTGRES_SCHEMA}.user_customer
                    WHERE id_user = :id_user
                """)

        result_get_id_customer = await session.execute(query_get_id_customer,
                                                       {"id_user": user.id})

        customerId = result_get_id_customer.mappings().first().id_customer

        return {"user": user, "customerId": customerId, "access_token": token, "token_type": "bearer"}

    async def delete_user_by_id(
        self,
        session: AsyncSession,
        id_user: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.users WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_user})
        deleted_row = result.fetchone()

        return True if deleted_row else False
