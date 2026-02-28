from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RETRIEVAL_THRESHOLD: float = 0.35
    TOP_K: int = 3
    OLLAMA_URL: str = "http://localhost:11434/api/generate"
    MODEL_NAME: str = "mistral"

settings = Settings()