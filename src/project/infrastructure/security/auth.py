from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from src.project.infrastructure.security.JWT_token import decode_access_token, TokenData
from src.project.core.config import settings

security = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = decode_access_token(
            token=token.credentials,
            secret=settings.JWT_SECRET_KEY.get_secret_value(),
            algorithm=settings.HASH_ALGORITHM
        )
        return payload  # возвращает данные из токена
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


async def allow_only_admin(current_user: TokenData = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    return current_user
