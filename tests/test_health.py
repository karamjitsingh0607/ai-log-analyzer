from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_ollama_available(monkeypatch):

    class MockClient:
        def list(self):
            return {
                "models": []
            }

    monkeypatch.setattr(
        "app.services.ollama_service.get_ollama_client",
        lambda: MockClient()
    )

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "AI Log Analyzer"
    assert data["ollama"]["status"] == "available"


def test_health_ollama_unavailable(monkeypatch):

    class MockClient:
        def list(self):
            raise Exception("Ollama unavailable")

    monkeypatch.setattr(
        "app.services.ollama_service.get_ollama_client",
        lambda: MockClient()
    )

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "degraded"
    assert data["service"] == "AI Log Analyzer"
    assert data["ollama"]["status"] == "unavailable"