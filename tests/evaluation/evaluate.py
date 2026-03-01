import requests

BASE_URL = "http://127.0.0.1:8000/query"

test_cases = [
    ("How do I rollback a deployment?", 200),
    ("How do I check if deployment is healthy?", 200),
    ("Explain quantum gravity", 422),
]

print("\n=== Meridian System Evaluation ===\n")

for query, expected_status in test_cases:
    response = requests.post(BASE_URL, json={"query": query})
    status = response.status_code

    try:
        body = response.json()
    except Exception:
        body = {}

    confidence = None
    if status == 200:
        confidence = body.get("confidence_score")
    elif status == 422:
        confidence = body.get("detail", {}).get("confidence_score")

    result = "PASS" if status == expected_status else "FAIL"

    print(f"Query: {query}")
    print(f"Expected: {expected_status} | Got: {status} | {result}")
    print(f"Confidence: {confidence}")
    print("-" * 50)