import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME", "GitLab Helper")
    secret_key: str = os.getenv("SECRET_KEY", "default_secret_key")
    fernet_key: bytes = bytes(os.getenv("FERNET_KEY", "default_fernet_key"), "utf-8")

    access_token_algorithm: str = os.getenv("ACCESS_TOKEN_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 5))
    refresh_token_expire_minutes: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60))


settings = Settings()
