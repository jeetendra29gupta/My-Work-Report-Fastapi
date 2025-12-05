import httpx

client = httpx.Client(
    base_url="http://127.0.0.1:8181",
    headers={
        "accept": "application/json",
        "Content-Type": "application/json",
    },
    timeout=10
)


def signup_user(payload: dict):
    response = client.post("/auth/signup", json=payload)
    response.raise_for_status()
    return response.json()
