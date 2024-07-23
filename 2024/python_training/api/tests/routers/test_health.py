from fastapi.testclient import TestClient


def test_health(test_client: TestClient) -> None:
    response = test_client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == "OK"
