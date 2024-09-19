from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """VPN settings"""

    vpn_port: str = "avatar"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="KAMI_",
        env_file_encoding="utf-8",
        extra="allow",
    )


def get_settings() -> Settings:
    """Get module settings"""

    return Settings()
