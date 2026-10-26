from fastapi.testclient import TestClient

from payflow.api import app


def test_api_health_and_routes():
    client = TestClient(app)
    assert client.get("/api/health").json()["live_rails"] is False
    assert len(client.get("/api/routes").json()) > 0


def test_api_evaluation_returns_decision():
    client = TestClient(app)
    response = client.post(
        "/api/payment/evaluate",
        json={"amount": 100000, "source_currency": "EUR", "destination_currency": "BRL"},
    )
    assert response.status_code == 200
    assert response.json()["decision"] == "ROUTE"
