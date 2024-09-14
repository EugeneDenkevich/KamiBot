from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for project"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="KAMI_BOT_",
        env_file_encoding="utf-8",
        extra="allow",
    )

    bot_token: str = ""


def get_settings() -> Settings:
    """Dependency for getting settings"""

    return Settings()
