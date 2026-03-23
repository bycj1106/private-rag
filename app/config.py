import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_api_key: str
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 5
    data_dir: str = "./data"
    chroma_dir: str = "./data/chroma"
    db_path: str = "./data/app.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
