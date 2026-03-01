import requests
from core.config import settings
from providers.base import LLMProvider

class OllamaProvider(LLMProvider):
    """
    Local inference provider using Ollama.
    Suitable for development environments.
    """

    def __init__(self, model: str, endpoint: str):
        self.model = model
        self.endpoint = endpoint

    def generate(self, prompt: str) -> str:
        response = requests.post(
            self.endpoint,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]