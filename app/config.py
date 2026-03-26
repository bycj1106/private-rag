from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="env/.env",
        env_file_encoding="utf-8"
    )

    openai_api_key: str
    minimax_api_url: str = "https://api.minimaxi.com/v1/text/chatcompletion_v2"
    chunk_size: int = Field(default=500, ge=100, le=100000)
    chunk_overlap: int = Field(default=50, ge=0, le=10000)
    top_k: int = Field(default=5, ge=1, le=100)
    data_dir: str = "./data"
    chroma_dir: str = "./data/chroma"
    db_path: str = "./data/app.db"
    ollama_base_url: str = "http://localhost:11434"
    ollama_embedding_model: str = "nomic-embed-text"
    use_local_embedding: bool = False
    api_retry_times: int = Field(default=3, ge=1, le=10)
    api_retry_delay: float = Field(default=1.0, ge=0.1, le=30.0)
    cors_origins: list[str] = Field(default=["http://localhost:5173", "http://127.0.0.1:5173"])

    @field_validator('minimax_api_url', 'ollama_base_url')
    @classmethod
    def validate_url(cls, v: str) -> str:
        v = v.strip()
        if not v.startswith('http://') and not v.startswith('https://'):
            raise ValueError('URL must start with http:// or https://')
        return v.rstrip('/')


@lru_cache()
def get_settings() -> Settings:
    return Settings()
