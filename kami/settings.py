from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    """Settings for project"""

    debug_mode: bool = False

    bot_client_token: str = ""
    bot_admin_token: str = ""

    db_host: str = ""
    db_port: int = 5432
    db_user: str = ""
    db_pass: str = ""
    db_name: str = ""

    client_language: str = "en"
    admin_language: str = "en"
    translation_language: str = "Italian"

    admin_id: str = ""

    context_limit: int = 5

    awaiting_time: int = 600

    vpn_conn_string: str = ""

    server_domain: str = ""
    server_host: str = ""
    server_port_client: int = 5000
    server_port_admin: int = 5001

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
