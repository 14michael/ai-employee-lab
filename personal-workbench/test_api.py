import os
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient

def test_api_crud_and_auth(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setenv("WORKBENCH_DB", str(Path(tmp) / "test.db"))
        monkeypatch.setenv("WORKBENCH_TOKEN", "test-secret")
        import importlib
        import api
        importlib.reload(api)
        client = TestClient(api.app)
        assert client.get("/api/health").status_code == 200
        assert client.get("/api/records/tasks").status_code == 401
        headers = {"Authorization": "Bearer test-secret"}
        created = client.post("/api/records", headers=headers,
                              json={"kind": "tasks", "title": "驗收", "body": "實測"})
        assert created.status_code == 201
        ident = created.json()["id"]
        assert len(client.get("/api/records/tasks", headers=headers).json()) == 1
        assert client.put(f"/api/records/{ident}", headers=headers,
                          json={"title": "驗收修正", "body": "已修改"}).status_code == 200
        assert client.patch(f"/api/records/{ident}/status", headers=headers,
                            json={"status": "done"}).status_code == 200
        assert client.get("/api/records/tasks", headers=headers).json()[0]["status"] == "done"
        assert client.delete(f"/api/records/{ident}", headers=headers).status_code == 200
        assert client.get("/api/records/tasks", headers=headers).json() == []
        assert client.post("/api/records", headers=headers,
                           json={"kind": "unknown", "title": "x"}).status_code == 400
