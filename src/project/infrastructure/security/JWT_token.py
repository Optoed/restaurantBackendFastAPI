import os

from jose import JWTError, jwt
from datetime import datetime, timedelta

from pydantic import BaseModel

from src.project.core.config import settings


class TokenData(BaseModel):
    user_id: int
    role: str


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode_data = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode_data.update({"exp": expire})

    # Convert SecretStr to string
    encoded_jwt = jwt.encode(to_encode_data,
                             settings.JWT_SECRET_KEY.get_secret_value(),
                             algorithm=settings.HASH_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str, secret: str, algorithm: str):
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        if payload.get("exp") < datetime.utcnow().timestamp():
            raise Exception("Token has expired")
        return TokenData(
            user_id=payload.get("user_id"),
            role=payload.get("role"),
        )
    except JWTError:
        raise Exception("Invalid token")
