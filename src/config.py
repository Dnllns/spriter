from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "Spriter"
    DATABASE_URL: str = "sqlite:///./spriter.db"
    # Default to SQLite for easy local dev, pluggable to Postgres
    STORAGE_PATH: str = "/tmp/spriter_uploads"

    # Auth (Placeholder for Phase 2b)
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"


settings = Settings()
