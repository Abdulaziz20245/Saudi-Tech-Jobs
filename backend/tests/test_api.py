from fastapi.testclient import TestClient

from app.main import app
from db.session import get_db


def test_health(session):
    app.dependency_overrides[get_db] = lambda: session
    try:
        response = TestClient(app).get("/api/health")
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "open_postings": 0}
