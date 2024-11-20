from pydantic_settings import BaseSettings
from pydantic import SecretStr, ValidationError

from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    ORIGINS: str = ""
    ROOT_PATH: str = ""
    ENV: str = ""
    LOG_LEVEL: str = ""

    POSTGRES_SCHEMA: str = "public"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_DB: str = "postgres"
    POSTGRES_PORT: int = 5433
    POSTGRES_USER: SecretStr = "postgres"
    POSTGRES_PASSWORD: SecretStr = "postgres"
    POSTGRES_RECONNECT_INTERVAL_SEC: int = 1

    @property
    def postgres_url(self) -> str:
        creds = f"{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}"
        return f"postgresql+asyncpg://{creds}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


try:
    settings = Settings()
    print("Настройки успешно загружены.")
    print("Postgres URL:", settings.postgres_url)
    print("ORIGINS:", settings.ORIGINS)
    print("ROOT_PATH:", settings.ROOT_PATH)
    # and so on for each variable
except ValidationError as e:
    print("Ошибка валидации:", e)

