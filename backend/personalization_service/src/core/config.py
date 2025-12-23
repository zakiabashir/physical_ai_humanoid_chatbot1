"""
Configuration settings for personalization service.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class PersonalizationConfig(BaseSettings):
    """Configuration for personalization service."""

    # Database
    database_url: str

    # Server
    host: str = "0.0.0.0"
    port: int = 8003

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global config instance
config = PersonalizationConfig()
