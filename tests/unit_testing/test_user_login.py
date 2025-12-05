import json
from unittest.mock import patch

import httpx
import pytest


def test_user_login():
    url = "http://127.0.0.1:8181/auth/login"

    payload = {
        "email_id": "jeetendra29gupta@example.com",
        "password": "jeetendra29gupta",
    }

    mock_response_data = {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY0NzY1OTIzfQ._dirI0T-kQKewmQuq3RamxoVJVAc2872w2H0vIJ318I",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY0ODUxNDIzfQ.ghDzX9n-IIoFNOqMGdzHSKw4Rft0A47uzjkXeIr0ZAU",
        "token_type": "bearer",
    }

    mock_response = httpx.Response(
        status_code=200,
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

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

    data = response.json()
    assert isinstance(data, dict)
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


if __name__ == "__main__":
    pytest.main()
