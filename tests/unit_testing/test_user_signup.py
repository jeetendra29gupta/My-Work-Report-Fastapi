import json
from unittest.mock import patch

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

    mock_response_data = {
        "id": 1,
        "full_name": payload["full_name"],
        "email_id": payload["email_id"],
        "role": "user",
        "created_at": "2025-12-03T10:59:40.526814",
        "updated_at": "2025-12-03T10:59:40.526814",
    }

    mock_response = httpx.Response(
        status_code=201,
        content=json.dumps(mock_response_data),
        headers={"content-type": "application/json"},
    )

    with patch.object(httpx.Client, "post", return_value=mock_response):
        with httpx.Client() as client:
            response = client.post(
                url,
                json=payload,
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                },
            )

    assert response.status_code == 201
    assert response.headers["content-type"].startswith("application/json")

    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] == 1
    assert data["full_name"] == payload["full_name"]
    assert data["email_id"] == payload["email_id"]
    assert data["role"] == "user"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


if __name__ == "__main__":
    pytest.main()
