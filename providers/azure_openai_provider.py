from providers.base import LLMProvider

class AzureOpenAIProvider(LLMProvider):
    """
    Azure OpenAI implementation placeholder.

    Intended integration:
    - Azure OpenAI Chat Completions API
    - Managed Identity or API key auth
    - Deployment-based model routing

    Future implementation would:
    - Use azure.identity for auth
    - Use azure.ai.openai SDK
    - Support deployment name configuration
    """

    def __init__(self, deployment_name: str):
        self.deployment_name = deployment_name

    def generate(self, prompt: str) -> str:
        raise NotImplementedError(
            "Azure OpenAI provider not yet implemented. "
            "This adapter is reserved for Azure production integration."
        )