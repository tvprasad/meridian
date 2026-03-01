from unittest.mock import patch

from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest

from api.main import app
from services.control.control_plane import handle_query

client = TestClient(app)


class FakeProvider:
    """Stub LLM provider that returns a fixed string, avoiding real model calls in tests."""

    def generate(self, _prompt: str) -> str:
        return "stubbed response"


def test_strong_match():
    """A query that matches indexed documents above threshold returns a well-formed answer."""
    response = handle_query(
        "How do I rollback a deployment?",
        provider_override=FakeProvider()
    )

    assert "trace_id" in response
    assert "answer" in response
    assert response["confidence_score"] >= 0.20


def test_irrelevant_query_refused():
    """A query with no relevant context is refused with HTTP 422 and a structured detail body."""
    with pytest.raises(HTTPException) as exc:
        handle_query(
            "Explain quantum gravity",
            provider_override=FakeProvider()
        )

    assert exc.value.status_code == 422
    assert exc.value.detail["reason"] == "Retrieval confidence below threshold"
    assert "trace_id" in exc.value.detail
    assert exc.value.detail["confidence_score"] < 0.20


def test_no_documents_refused():
    """When the retrieval store returns no documents at all, the request is refused with HTTP 422."""
    empty_results = {"documents": [], "distances": []}

    with patch("services.control.control_plane.query_documents", return_value=empty_results):
        with pytest.raises(HTTPException) as exc:
            handle_query("anything", provider_override=FakeProvider())

    assert exc.value.status_code == 422
    assert exc.value.detail["reason"] == "No documents retrieved"
    assert exc.value.detail["confidence_score"] == 0.0


def test_refusal_schema():
    """The HTTP /query endpoint exposes the expected error schema on refusal."""
    response = client.post("/query", json={"query": "Explain quantum gravity"})
    body = response.json()

    assert response.status_code == 422
    assert "detail" in body
    assert "trace_id" in body["detail"]
    assert "confidence_score" in body["detail"]
