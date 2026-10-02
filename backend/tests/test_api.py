import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "vector_store_ready" in data
    assert "document_count" in data


def test_query_empty_body():
    resp = client.post("/api/v1/query", json={})
    assert resp.status_code == 422


def test_query_short_question():
    resp = client.post("/api/v1/query", json={"question": "ab"})
    assert resp.status_code == 422


def test_query_missing_question():
    resp = client.post("/api/v1/query", json={"wrong_field": "hello"})
    assert resp.status_code == 422


def test_sources_endpoint():
    resp = client.get("/api/v1/sources")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
