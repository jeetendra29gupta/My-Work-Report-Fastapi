import httpx
import pytest


def test_user_signup():
    url = "http://127.0.0.1:8181/auth/signup"

    payload = {
        "full_name": "Jeetendra Gupta",
        "email_id": "jeetendra29gupta@example.com",
        "phone_no": "+91 0000000010",
        "password": "jeetendra29gupta",
    }

    with httpx.Client() as client:
        response = client.post(
            url,
            json=payload,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    assert response.headers["content-type"].startswith("application/json")
    assert response.status_code == 201

    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] > 0
    assert data["full_name"] == payload["full_name"]
    assert data["email_id"] == payload["email_id"]
    assert data["role"] == "user"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


if __name__ == "__main__":
    pytest.main()
