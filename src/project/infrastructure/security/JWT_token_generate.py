import os

from jose import JWTError, jwt
from datetime import datetime, timedelta


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()

    access_token_expire_minutes = float(os.getenv("ACCESS_JWT_TOKEN_EXPIRE_MINUTES"))
    if not access_token_expire_minutes:
        raise ValueError("ACCESS_JWT_TOKEN_EXPIRE_MINUTES is not set in the environment variables.")

    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise ValueError("JWT_SECRET_KEY is not set in the environment variables.")

    algorithm = os.getenv("HASH_ALGORITHM")
    if not algorithm:
        raise ValueError("HASH_ALGORITHM is not set in the environment variables.")

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt
