import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "knowledge_base")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    CHUNK_MIN_SIZE: int = 200
    CHUNK_MAX_SIZE: int = 1500
    CHUNK_BREAKPOINT_THRESHOLD_TYPE: str = "percentile"

    class Config:
        env_file = ".env"


settings = Settings()
