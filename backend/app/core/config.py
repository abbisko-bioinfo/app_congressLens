from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://congresslens:congresslens-password@localhost:5432/congresslens"
    minio_endpoint: str = "localhost:9000"
    minio_public_endpoint: str = "localhost:9000"
    minio_access_key: str = "congresslens"
    minio_secret_key: str = "congresslens-password"
    minio_bucket: str = "congresslens-attachments"
    minio_secure: bool = False
    backend_cors_origins: str = "http://localhost:5174"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",")]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()