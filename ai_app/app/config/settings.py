"""
Configuration settings for the EduSense AI application.
Manages environment variables and application settings.
"""

from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        google_api_key: Google Gemini AI API key
        app_name: Application name
        app_version: Application version
        debug_mode: Debug mode flag
        host: Server host address
        port: Server port
    """
    
    # Google Gemini AI Configuration
    google_api_key: str
    
    # Application Configuration
    app_name: str = "EduSense AI"
    app_version: str = "1.0.0"
    debug_mode: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS Configuration: comma-separated list of allowed origins, e.g.
    # "http://localhost:3000,https://myapp.com". Defaults to "*" (no credentials).
    cors_origins: str = "*"

    # Model Configuration
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

