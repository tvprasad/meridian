import requests

BASE_URL = "http://localhost:8000/query"

test_cases = [
    ("How do I rollback a deployment?", 200),
    ("How do I check if deployment is healthy?", 200),
    ("Explain quantum gravity", 422),
]

for query, expected in test_cases:
    response = requests.post(BASE_URL, json={"query": query})
    status = response.status_code
    result = "PASS" if status == expected else "FAIL"
    print(f"{query} → {status} → {result}")