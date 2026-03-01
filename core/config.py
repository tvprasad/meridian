from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RETRIEVAL_THRESHOLD: float = 0.20
    TOP_K: int = 3
    OLLAMA_URL: str = "http://localhost:11434/api/generate"
    MODEL_NAME: str = "mistral"
    LLM_PROVIDER: str = "local"  # local | azure
    AZURE_DEPLOYMENT_NAME: str = "gpt-4o"

settings = Settings()