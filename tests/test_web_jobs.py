import os
from fastapi.testclient import TestClient
from herbarium_processor.web import main as webmain


def test_list_jobs(tmp_path, monkeypatch):
    monkeypatch.setattr(webmain, "TMP_DIR", tmp_path)
    (tmp_path / "job_foo").mkdir()
    (tmp_path / "job_bar").mkdir()

    client = TestClient(webmain.app)
    resp = client.get("/jobs")
    assert resp.status_code == 200
    data = resp.json()
    assert set(data["jobs"]) == {"foo", "bar"}

