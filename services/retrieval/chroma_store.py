import chromadb
from sentence_transformers import SentenceTransformer
from core.config import settings

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("meridian")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def add_document(doc_id: str, text: str):
    embedding = embedder.encode(text).tolist()
    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[doc_id]
    )

def query_documents(query: str):
    query_embedding = embedder.encode(query).tolist()    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=settings.TOP_K
    )
    return results