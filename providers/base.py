from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """
    Abstract LLM provider interface.

    This allows Meridian to swap between:
    - Local Ollama
    - Azure OpenAI
    - OpenAI API
    - Bedrock
    - Future internal LLM services

    The control plane remains model-agnostic.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass