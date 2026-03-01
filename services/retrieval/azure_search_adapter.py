from services.retrieval.base import RetrievalAdapter

class AzureCognitiveSearchAdapter(RetrievalAdapter):
    """
    Placeholder for Azure Cognitive Search integration.

    Intended design:
    - Hybrid search (BM25 + vector)
    - Metadata filtering
    - Semantic ranking
    - Index-per-tenant strategy (future SaaS)

    Would integrate:
    - azure-search-documents SDK
    - Vector index configuration
    - Role-based filtering
    """

    def query(self, text: str):
        raise NotImplementedError(
            "Azure Cognitive Search adapter not implemented yet."
        )