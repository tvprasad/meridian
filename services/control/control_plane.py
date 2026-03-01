import uuid
from fastapi import HTTPException
from core.config import settings
from core.logging import log_event
from services.retrieval.chroma_store import query_documents
from providers.ollama_provider import OllamaProvider
from providers.azure_openai_provider import AzureOpenAIProvider


def get_provider():
    """
    Config-driven provider selection.

    Supports:
    - local (Ollama)
    - azure (Azure OpenAI)
    """

    if settings.LLM_PROVIDER == "azure":
        return AzureOpenAIProvider(
            deployment_name=settings.AZURE_DEPLOYMENT_NAME
        )

    return OllamaProvider(
        model=settings.MODEL_NAME,
        endpoint=settings.OLLAMA_URL
    )


def handle_query(user_query: str, provider_override=None):
    trace_id = str(uuid.uuid4())
    provider = provider_override if provider_override else get_provider()

    results = query_documents(user_query)

    if not results["documents"]:
        event = {
            "trace_id": trace_id,
            "query": user_query,
            "retrieval_scores": [],
            "threshold": settings.RETRIEVAL_THRESHOLD,
            "confidence_score": 0.0,
            "decision": "REFUSED",
            "refusal_reason": "No documents retrieved"
        }
        log_event(event)

        raise HTTPException(
            status_code=422,
            detail={
                "trace_id": trace_id,
                "reason": "No documents retrieved",
                "confidence_score": 0.0
            }
        )

    # Convert Chroma distances to similarity scores
    distances = results.get("distances", [[]])[0]
    scores = [1 - d for d in distances]
    confidence = max(scores) if scores else 0.0

    if confidence < settings.RETRIEVAL_THRESHOLD:
        event = {
            "trace_id": trace_id,
            "query": user_query,
            "retrieval_scores": scores,
            "threshold": settings.RETRIEVAL_THRESHOLD,
            "confidence_score": confidence,
            "decision": "REFUSED",
            "refusal_reason": "Retrieval confidence below threshold"
        }
        log_event(event)

        raise HTTPException(
            status_code=422,
            detail={
                "trace_id": trace_id,
                "reason": "Retrieval confidence below threshold",
                "confidence_score": confidence
            }
        )

    context = "\n".join(results["documents"][0])

    prompt = f"""
    Answer the question using only the provided context.
    Provide citations if applicable.

    Context:
    {context}

    Question:
    {user_query}
    """

    answer = provider.generate(prompt)

    event = {
        "trace_id": trace_id,
        "query": user_query,
        "retrieval_scores": scores,
        "threshold": settings.RETRIEVAL_THRESHOLD,
        "confidence_score": confidence,
        "decision": "OK",
        "refusal_reason": None
    }
    log_event(event)

    return {
        "trace_id": trace_id,
        "answer": answer,
        "confidence_score": confidence
    }