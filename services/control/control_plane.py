from core.config import settings
from services.retrieval.chroma_store import query_documents
from providers.ollama_provider import generate_response

def handle_query(user_query: str):
    results = query_documents(user_query)

    if not results["documents"]:
        return {
            "status": "REFUSED",
            "reason": "No documents retrieved",
            "confidence_score": 0.0
        }

    top_score = results["distances"][0][0] if results["distances"] else 0.0
    confidence = 1 - top_score  # simple transform

    if confidence < settings.RETRIEVAL_THRESHOLD:
        return {
            "status": "REFUSED",
            "reason": "Retrieval confidence below threshold",
            "confidence_score": confidence
        }

    context = "\n".join(results["documents"][0])

    prompt = f"""
    Answer the question using only the provided context.
    Provide citations if applicable.

    Context:
    {context}

    Question:
    {user_query}
    """

    answer = generate_response(prompt)

    return {
        "status": "OK",
        "answer": answer,
        "confidence_score": confidence
    }