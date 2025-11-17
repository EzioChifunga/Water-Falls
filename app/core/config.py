"""
Configurações da aplicação
"""
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação FastAPI

    This Settings class loads environment variables from `.env` and accepts
    both a full `DATABASE_URL` or individual DB parts such as
    `DATABASE_USER`, `DATABASE_PASSWORD`, etc. It also tolerates extra
    environment variables (so the .env may include other keys without
    raising `extra_forbidden`).
    """

    # Database: accept either a full URL or parts
    database_url: Optional[str] = None
    database_user: Optional[str] = None
    database_password: Optional[str] = None
    database_host: Optional[str] = None
    database_port: Optional[int] = None
    database_name: Optional[str] = None
    database_sslmode: Optional[str] = None

    # API
    api_title: str = "WaterFalls API"
    api_version: str = "1.0.0"
    api_description: str = "API para gerenciamento de carros"

    # Server
    server_host: str = "0.0.0.0"
    server_port: int = 8000

    # pydantic v2 settings: read .env and ignore extra variables
    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }

    def get_database_url(self) -> str:
        """Return the DB URL. Prefer `database_url` if set, otherwise build
        from the individual components (user/password/host/port/name).
        """
        if self.database_url:
            return self.database_url

        # minimal builder for a PostgreSQL URL
        user = self.database_user or ""
        pwd = self.database_password or ""
        host = self.database_host or "localhost"
        port = self.database_port or 5432
        name = self.database_name or ""
        ssl = self.database_sslmode

        auth = f"{user}:{pwd}@" if user or pwd else ""
        url = f"postgresql://{auth}{host}:{port}/{name}"
        if ssl:
            url = f"{url}?sslmode={ssl}"
        return url


settings = Settings()

# convenience constant used by the rest of the app
DATABASE_URL = settings.get_database_url()
