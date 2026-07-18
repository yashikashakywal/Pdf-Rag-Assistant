
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Groq
    groq_api_key: str = ""
    # LLM
    llm_model_name: str = "llama-3.3-70b-versatile"
    # -- Embeddings --
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    # -- Retrieval --
    chunk_size: int = 800
    chunk_overlap: int = 150
    retrieval_k: int = 3

    # -- Storage paths --
    # Each of these is a per-user subfolder created at runtime, e.g.
    # app/data/uploads/<user_id>/ and app/data/faiss_index/<user_id>/
    upload_dir: str = "app/data/uploads"
    faiss_index_dir: str = "app/data/faiss_index"

    # -- CORS --
    allowed_origins: str = "http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000"

    # -- Auth --
    # Generate a real secret with: python -c "import secrets; print(secrets.token_hex(32))"
    # and set it via the JWT_SECRET_KEY env var in production — never rely on this default.
    jwt_secret_key: str = "dev-only-insecure-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    # -- Database (stores user accounts only) --
    database_url: str = "sqlite:///./app/data/app.db"

    # -- Password reset emails (via Resend, https://resend.com) --
    resend_api_key: str = ""
    # Resend's shared sandbox sender — works immediately with no setup, but
    # only delivers to the email you signed up to Resend with. Once you verify
    # your own domain in the Resend dashboard, switch this to an address on
    # that domain (e.g. "Marginalia <noreply@yourdomain.com>") to email anyone.
    email_from: str = "Marginalia <onboarding@resend.dev>"
    # Where reset links point users back to — set this to your deployed
    # frontend URL in production (e.g. https://pdf-rag-assistant-17ne.onrender.com)
    frontend_base_url: str = "http://localhost:5500"
    password_reset_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


settings = Settings()
