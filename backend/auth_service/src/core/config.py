"""
Configuration settings for auth service.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class AuthConfig(BaseSettings):
    """Configuration for authentication service."""

    # Database
    database_url: str

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 10080  # 7 days

    # Email (Resend)
    resend_api_key: Optional[str] = None
    resend_from_email: str = "noreply@yourdomain.com"
    frontend_url: str = "http://localhost:3000"

    # OAuth
    oauth_google_client_id: Optional[str] = None
    oauth_google_client_secret: Optional[str] = None
    oauth_google_redirect_uri: str = "http://localhost:3000/auth/callback/google"

    oauth_github_client_id: Optional[str] = None
    oauth_github_client_secret: Optional[str] = None
    oauth_github_redirect_uri: str = "http://localhost:3000/auth/callback/github"

    # Server
    host: str = "0.0.0.0"
    port: int = 8001

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global config instance
config = AuthConfig()
