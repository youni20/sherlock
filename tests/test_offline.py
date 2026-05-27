# Offline tests for the /get_answer logic — no API key, no network.
# Lazy client init (get_vector_store / get_model) lets us import the app and
# patch out the real Gemini/Chroma calls, so we can test the source-parsing
# logic in main.py deterministically.

from fastapi.testclient import TestClient

import main


def _patch(monkeypatch, raw: str, retrieved_sources: list[str]) -> None:
    monkeypatch.setattr(main, "get_vector_store", lambda: None)
    monkeypatch.setattr(
        main, "retrieve_context_with_sources", lambda vector_store, question: ("context", retrieved_sources)
    )
    monkeypatch.setattr(main, "ask_question", lambda question, docs: raw)


client = TestClient(main.app)


def test_answer_keeps_only_retrieved_sources(monkeypatch):
    # Model cites case.txt (retrieved) and ghost.txt (not retrieved) -> ghost.txt is dropped
    _patch(monkeypatch, "The butler was in the garden.\nSOURCES: case.txt, ghost.txt", ["case.txt", "other.txt"])

    data = client.post("/get_answer", json={"question": "Where was the butler?"}).json()

    assert data["answer"] == "The butler was in the garden."
    assert data["sources"] == ["case.txt"]


def test_abstention_returns_no_sources(monkeypatch):
    _patch(monkeypatch, "I don't have enough evidence to answer that.\nSOURCES: none", ["case.txt"])

    data = client.post("/get_answer", json={"question": "Who did it?"}).json()

    assert data["answer"] == "I don't have enough evidence to answer that."
    assert data["sources"] == []


def test_bad_file_extension_rejected():
    r = client.post("/ingest_file", files={"file": ("case.png", b"\x89PNG", "image/png")})
    assert r.status_code == 400
