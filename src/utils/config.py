from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Example settings, add more as needed
    server: str
    database: str
    environment: str = "dev"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings() 