from fastapi.testclient import TestClient

from herbarium_processor.web.main import app


def test_redirect_www_to_apex():
    client = TestClient(app)
    response = client.get(
        "/", headers={"host": "www.example.com"}, follow_redirects=False
    )
    assert response.status_code == 301
    assert response.headers["location"] == "http://example.com/"
