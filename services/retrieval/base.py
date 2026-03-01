from abc import ABC, abstractmethod
from typing import List

class RetrievalAdapter(ABC):
    """
    Abstract retrieval interface.

    Enables swapping:
    - Chroma (local)
    - Azure Cognitive Search
    - Elastic
    - Pinecone
    """

    @abstractmethod
    def query(self, text: str) -> List[float]:
        pass