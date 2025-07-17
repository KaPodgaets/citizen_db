from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Example settings, add more as needed
    server: str = "localhost_placeholder"
    database: str = "mydb_placeholder"
    environment: str = "dev"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    transformation_retries_default: int = 2

settings = Settings() 