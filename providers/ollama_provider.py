import requests
from core.config import settings

def generate_response(prompt: str):
    response = requests.post(
        settings.OLLAMA_URL,
        json={
            "model": settings.MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]