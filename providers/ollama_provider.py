import requests
from providers.base import LLMProvider

class OllamaProvider(LLMProvider):
    """
    Local inference provider using Ollama.
    Suitable for development environments.
    """

    def __init__(self, model: str, endpoint: str):
        # Store the model name and API endpoint for use in generate()
        self.model = model
        self.endpoint = endpoint

    def generate(self, prompt: str) -> str:
        # POST the prompt to the Ollama API with streaming disabled
        # so we receive a single complete response object
        response = requests.post(
            self.endpoint,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False  # disable token streaming; get full response at once
            }
        )
        # Extract and return the generated text from the response payload
        return response.json()["response"]