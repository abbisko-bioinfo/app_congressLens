from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+psycopg://congresslens:congresslens-password@localhost:5432/congresslens"

    # MinIO
    minio_endpoint: str = "localhost:9000"
    minio_public_endpoint: str = "localhost:9000"
    minio_access_key: str = "congresslens"
    minio_secret_key: str = "congresslens-password"
    minio_bucket: str = "congresslens-attachments"
    minio_secure: bool = False

    # CORS
    backend_cors_origins: str = "http://localhost:5174"

    # Auth
    secret_key: str = "change-me-in-production-use-env-var"
    ldap_enabled: bool = False
    ldap_server: str = ""
    ldap_bind_dn_template: str = ""
    ldap_search_base: str = ""
    ldap_user_filter: str = ""
    admin_users: str = ""

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",")]

    @property
    def admin_users_list(self) -> list[str]:
        return [u.strip() for u in self.admin_users.split(",") if u.strip()]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
