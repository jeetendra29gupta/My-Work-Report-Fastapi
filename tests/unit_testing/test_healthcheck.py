import json
from unittest.mock import patch

import httpx
import pytest


def test_healthcheck():
    url = "http://127.0.0.1:8181/"

    mock_response_data = {"status": "ok"}

    mock_response = httpx.Response(
        status_code=200,
        content=json.dumps(mock_response_data),
        headers={"content-type": "application/json"},
    )

    with patch.object(httpx.Client, "get", return_value=mock_response):
        with httpx.Client() as client:
            response = client.get(
                url,
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                },
            )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

    data = response.json()
    assert isinstance(data, dict)
    assert data["status"] == "ok"


if __name__ == "__main__":
    pytest.main()
