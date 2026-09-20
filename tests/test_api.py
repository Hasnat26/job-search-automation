from pathlib import Path

from fastapi.testclient import TestClient

from backend.api import app


client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_rejects_unsupported_extension():
    response = client.post(
        "/api/cv",
        files={"file": ("resume.exe", b"not a cv", "application/octet-stream")},
    )
    assert response.status_code == 400
    assert "Supported CV formats" in response.json()["detail"]


def test_upload_rejects_empty_file():
    response = client.post(
        "/api/cv",
        files={"file": ("resume.txt", b"", "text/plain")},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "The uploaded CV is empty"


def test_upload_calls_ingestion(monkeypatch):
    captured = {}

    def fake_ingest(path, db_path, model):
        captured["path"] = Path(path)
        captured["db_path"] = db_path
        captured["model"] = model
        return {"document_id": 1, "profile_id": 1, "duplicate": False}

    monkeypatch.setattr("backend.api.ingest_cv", fake_ingest)

    response = client.post(
        "/api/cv",
        files={"file": ("resume.txt", b"test cv", "text/plain")},
    )

    assert response.status_code == 200
    assert response.json()["profile_id"] == 1
    assert captured["path"].name == "resume.txt"
    assert not captured["path"].exists()
