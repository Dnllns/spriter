from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "Spriter"
    DATABASE_URL: str = "sqlite:///./spriter.db"
    # Default to SQLite for easy local dev, pluggable to Postgres
    STORAGE_PATH: str = "/tmp/spriter_uploads"

    # Auth (OIDC)
    OIDC_ISSUER: str = "https://your-oidc-provider.com"
    OIDC_AUDIENCE: str = "spriter-api"

    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"


settings = Settings()
