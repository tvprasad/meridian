from services.retrieval.chroma_store import add_document

def seed_documents():
    add_document(
        "runbook-rollback",
        "To rollback a deployment, revert to previous stable version and restart the service."
    )
    add_document(
        "runbook-health-check",
        "To validate deployment health, check logs and ensure all services return HTTP 200."
    )

if __name__ == "__main__":
    seed_documents()
    print("Documents seeded.")