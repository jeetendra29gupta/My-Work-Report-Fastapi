import httpx
import pytest


def test_user_login():
    url = "http://127.0.0.1:8181/auth/login"

    payload = {
        "email_id": "jeetendra29gupta@example.com",
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
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


if __name__ == "__main__":
    pytest.main()
