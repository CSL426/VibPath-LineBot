"""
Environment Configuration Management
Centralized configuration using Pydantic for validation and type safety
"""
import os
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Centralized environment configuration with validation"""

    # LINE Bot Configuration
    channel_secret: str = Field(..., alias="ChannelSecret", description="LINE Bot Channel Secret")
    channel_access_token: str = Field(..., alias="ChannelAccessToken", description="LINE Bot Channel Access Token")

    # Google AI Configuration
    google_api_key: str = Field(..., alias="GOOGLE_API_KEY", description="Google AI API Key")

    # MongoDB Configuration
    mongodb_uri: Optional[str] = Field(None, alias="MONGODB_URI", description="Complete MongoDB URI")
    mongodb_username: Optional[str] = Field(None, alias="MONGODB_USERNAME", description="MongoDB Username")
    mongodb_password: Optional[str] = Field(None, alias="MONGODB_PASSWORD", description="MongoDB Password")
    mongodb_cluster: Optional[str] = Field(None, alias="MONGODB_CLUSTER", description="MongoDB Cluster URL")
    mongodb_database: str = Field(default="vibpath_linebot", alias="MONGODB_DATABASE", description="MongoDB Database Name")
    mongodb_app_name: str = Field(default="vibpath", alias="MONGODB_APP_NAME", description="MongoDB App Name")

    # Admin Configuration
    admin_user_ids: str = Field(default="", alias="ADMIN_USER_IDS", description="Colon-separated admin user IDs")

    # Server Configuration
    port: int = Field(default=8080, alias="PORT", description="Server port")

    # Google Cloud Configuration (optional)
    google_cloud_project: Optional[str] = Field(None, alias="GOOGLE_CLOUD_PROJECT", description="Google Cloud Project ID")
    service_name: Optional[str] = Field(None, alias="SERVICE_NAME", description="Cloud Run Service Name")

    # Static Resources (optional)
    static_base_url: Optional[str] = Field(None, alias="STATIC_BASE_URL", description="Static resources base URL")

    # Timezone (optional)
    timezone: str = Field(default="UTC", alias="TIMEZONE", description="Application timezone")

    @field_validator("channel_secret")
    @classmethod
    def validate_channel_secret(cls, v: str) -> str:
        """Validate LINE channel secret is not empty"""
        if not v or v.strip() == "":
            raise ValueError("ChannelSecret cannot be empty")
        return v

    @field_validator("channel_access_token")
    @classmethod
    def validate_channel_access_token(cls, v: str) -> str:
        """Validate LINE channel access token is not empty"""
        if not v or v.strip() == "":
            raise ValueError("ChannelAccessToken cannot be empty")
        return v

    @field_validator("google_api_key")
    @classmethod
    def validate_google_api_key(cls, v: str) -> str:
        """Validate Google API key is not empty"""
        if not v or v.strip() == "":
            raise ValueError("GOOGLE_API_KEY cannot be empty")
        return v

    def get_mongodb_uri(self) -> Optional[str]:
        """
        Get MongoDB URI - either from direct URI or build from components

        Returns:
            Optional[str]: MongoDB connection URI or None if not configured
        """
        if self.mongodb_uri:
            return self.mongodb_uri

        # Build URI from components
        if self.mongodb_username and self.mongodb_password and self.mongodb_cluster:
            return (
                f"mongodb+srv://{self.mongodb_username}:{self.mongodb_password}"
                f"@{self.mongodb_cluster}/?retryWrites=true&w=majority"
                f"&appName={self.mongodb_app_name}"
            )

        return None

    def is_mongodb_configured(self) -> bool:
        """Check if MongoDB is properly configured"""
        return self.get_mongodb_uri() is not None

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"  # Ignore extra fields in .env
    }


# Global settings instance
try:
    settings = Settings()
    print("[OK] Environment configuration loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load environment configuration: {e}")
    raise
