from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "Homelab Notes+Tasks"
    APP_ENV: str = "dev"
    SECRET_KEY: str = "change-me"
    BASE_URL: str = "http://localhost:8000"

    DATABASE_URL: str = "postgresql+psycopg://app:app@localhost:5432/app"

    STORAGE_BACKEND: str = "local"  # local | s3
    LOCAL_STORAGE_PATH: str = "/data/uploads"

    SEARCH_BACKEND: str = "simple"  # simple | postgres_fts | meilisearch
    JOBS_BACKEND: str = "inline"    # inline | redis

settings = Settings()
