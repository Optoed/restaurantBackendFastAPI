from pydantic_settings import BaseSettings
from pydantic import SecretStr, ValidationError

from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    ORIGINS: str = ""
    ROOT_PATH: str = ""
    ENV: str = ""
    LOG_LEVEL: str = ""

    POSTGRES_SCHEMA: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_USER: SecretStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_RECONNECT_INTERVAL_SEC: int = 1

    # JWT tokens
    JWT_SECRET_KEY: SecretStr  # чтобы скрыть значение при логах
    HASH_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def postgres_url(self) -> str:
        creds = f"{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}"
        return f"postgresql+asyncpg://{creds}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


try:
    settings = Settings()
    print("Настройки успешно загружены.")
except ValidationError as e:
    print("Ошибка валидации:", e)
