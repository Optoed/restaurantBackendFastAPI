from fastapi import APIRouter

from project.infrastructure.postgres.repository.user_repo import UserRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.user import UserSchema


router = APIRouter()
