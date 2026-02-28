import uuid
from core.config import settings
from core.logging import log_event
from services.retrieval.chroma_store import query_documents
from providers.ollama_provider import generate_response
from fastapi import HTTPException


def handle_query(user_query: str):
    trace_id = str(uuid.uuid4())

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

        raise HTTPException(status_code=404, detail={
            "trace_id": trace_id,
            "reason": "No documents retrieved",
            "confidence_score": 0.0
        })

    # Chroma returns distances — lower is better
    distances = results.get("distances", [[]])[0]
    scores = [1 - d for d in distances]  # transform to confidence-like score
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

        raise HTTPException(status_code=422, detail={
            "trace_id": trace_id,
            "reason": "Retrieval confidence below threshold",
            "confidence_score": confidence
        })

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

    raise HTTPException(status_code=200, detail={
        "trace_id": trace_id,
        "answer": answer,
        "confidence_score": confidence
    })
