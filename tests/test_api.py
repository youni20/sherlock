import io
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home_returns_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_get_files_returns_list():
    response = client.get("/get_files")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.integration
def test_ingest_txt_file():
    content = b"This is a test case file with witness statements."
    response = client.post(
        "/ingest_file",
        files={"file": ("test_case.txt", io.BytesIO(content), "text/plain")},
    )
    assert response.status_code == 200
    assert response.json()["filename"] == "test_case.txt"


@pytest.mark.integration
def test_get_answer_returns_answer_and_sources():
    response = client.post("/get_answer", json={"question": "What happened?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
