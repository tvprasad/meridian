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

    # Use Azure OpenAI when explicitly configured; fall back to local Ollama
    if settings.LLM_PROVIDER == "azure":
        return AzureOpenAIProvider(
            deployment_name=settings.AZURE_DEPLOYMENT_NAME
        )

    # Default: local Ollama instance using model name and URL from settings
    return OllamaProvider(
        model=settings.MODEL_NAME,
        endpoint=settings.OLLAMA_URL
    )


def handle_query(user_query: str, provider_override=None):
    """
    Orchestrate a RAG query end-to-end.

    Retrieves relevant documents from Chroma, checks retrieval confidence
    against the configured threshold, builds a grounded prompt, calls the
    LLM provider, and returns the answer with tracing metadata.

    Args:
        user_query: The natural-language question from the user.
        provider_override: Optional LLMProvider instance to use instead of
            the config-driven default (primarily for testing).

    Returns:
        dict with keys:
            - trace_id (str): UUID for correlating logs.
            - answer (str): LLM-generated response grounded in retrieved context.
            - confidence_score (float): Highest retrieval similarity score (0–1).

    Raises:
        HTTPException(422): If no documents are retrieved or the best
            retrieval score falls below ``settings.RETRIEVAL_THRESHOLD``.
    """
    # Unique ID used to correlate this request across logs and the response
    trace_id = str(uuid.uuid4())

    # Allow callers (e.g. tests) to inject a provider; otherwise use config
    provider = provider_override if provider_override else get_provider()

    # Query the vector store for documents relevant to the user's question
    results = query_documents(user_query)

    # Guard: refuse immediately if Chroma returned no documents at all
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

    # Chroma returns L2 distances; convert to similarity scores (0–1)
    distances = results.get("distances", [[]])[0]
    scores = [1 - d for d in distances]

    # Take the highest similarity score as the overall retrieval confidence
    confidence = max(scores) if scores else 0.0

    # Guard: refuse if the best match is still below the confidence threshold
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

    # Flatten retrieved document chunks into a single context block
    context = "\n".join(results["documents"][0])

    # Build a grounded prompt that restricts the LLM to the retrieved context
    prompt = f"""
    Answer the question using only the provided context.
    Provide citations if applicable.

    Context:
    {context}

    Question:
    {user_query}
    """

    # Call the LLM provider to generate an answer from the grounded prompt
    answer = provider.generate(prompt)

    # Log a successful query event before returning
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
