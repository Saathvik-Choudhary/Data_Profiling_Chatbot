"""Configuration management for the data profiling chatbot."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database settings (with defaults for testing)
    # Use 'profiling_sample' to use SQLite for local development
    db_server: str = "localhost"
    db_database: str = "profiling_sample"  # Use SQLite by default
    db_username: str = "test_user"
    db_password: str = "test_password"
    db_driver: str = "ODBC Driver 17 for SQL Server"
    
    # Ollama settings
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"  # Upgraded to more powerful model
    
    # Application settings
    log_level: str = "INFO"
    
    # Allowed database views (security constraint)
    allowed_views: list[str] = [
        "profiling_column_stats",
        "profiling_table_stats",
        "profiling_data_quality"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

