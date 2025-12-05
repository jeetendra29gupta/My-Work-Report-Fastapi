import httpx
import pytest


def test_healthcheck():
    url = "http://127.0.0.1:8181/"

    with httpx.Client() as client:
        response = client.get(url, headers={"accept": "application/json"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

    data = response.json()
    assert isinstance(data, dict)
    assert data["status"] == "ok"


if __name__ == "__main__":
    pytest.main()
