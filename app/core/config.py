from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application configuration.

    Loads values from the .env file and exposes them
    throughout the application via a singleton object.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # -------------------------
    # Application
    # -------------------------

    app_name: str = "Kyroo"
    app_version: str = "1.0.0"
    environment: str = Field(default="development")

    # -------------------------
    # Database
    # -------------------------

    database_url: str

    # -------------------------
    # LLM
    # -------------------------

    llm_provider: str = "anthropic"

    anthropic_api_key: str = ""

    openai_api_key: str = ""

    gemini_api_key: str = ""

    openrouter_api_key: str = ""

    # -------------------------
    # WhatsApp
    # -------------------------

    whatsapp_token: str = ""

    phone_number_id: str = ""

    verify_token: str = ""

    # -------------------------
    # Security
    # -------------------------

    secret_key: str = ""

    algorithm: str = "HS256"


@lru_cache
def get_settings() -> Settings:
    """
    Returns one cached Settings instance.
    """
    return Settings()


settings = get_settings()