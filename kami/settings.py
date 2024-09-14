from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    """Settings for project"""

    bot_token: str = ""

    db_host: str = ""
    db_port: int = 5432
    db_user: str = ""
    db_pass: str = ""
    db_name: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="KAMI_BOT_",
        env_file_encoding="utf-8",
        extra="allow",
    )

    def get_db_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            username=self.db_user,
            password=self.db_pass,
            database=self.db_name,
        )


def get_settings() -> Settings:
    """Get project settings"""

    return Settings()
