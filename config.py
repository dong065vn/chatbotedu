"""
Configuration Management - Centralized Settings
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

# Base directory
BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "Chatbot Quản lý Thời gian"
    APP_VERSION: str = "2.0.0"
    APP_DESCRIPTION: str = "AI Chatbot with Gemini - Smart schedule and study management"
    DEBUG: bool = False
    ENV: str = "production"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    LOG_LEVEL: str = "info"
    
    # Database
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/chatbot.db"
    DATABASE_ECHO: bool = False
    
    # AI Integration
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-pro"
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 1024
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    CORS_ORIGINS: list = ["*"]
    ALLOWED_HOSTS: list = ["*"]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Cache
    CACHE_TTL: int = 3600  # 1 hour
    
    # File Uploads (future feature)
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: set = {".txt", ".pdf", ".docx"}
    
    # Static Files
    STATIC_DIR: Path = BASE_DIR / "static"
    
    # Logging
    LOG_FILE: Path = BASE_DIR / "logs" / "app.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Create necessary directories
def init_directories():
    """Initialize required directories"""
    directories = [
        settings.STATIC_DIR,
        settings.LOG_FILE.parent,
        BASE_DIR / "data",
        BASE_DIR / "backups"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Initialize on import
init_directories()

# Export settings
__all__ = ["settings", "Settings", "BASE_DIR"]