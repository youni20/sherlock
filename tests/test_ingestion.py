import pytest
from ingestion import split_text, load_document


def test_split_text_returns_chunks():
    text = "word " * 1000
    chunks = split_text(text)
    assert len(chunks) > 0


def test_split_text_empty_input():
    chunks = split_text("")
    assert chunks == []


def test_split_text_chunk_size():
    text = "word " * 1000
    chunks = split_text(text)
    for chunk in chunks:
        assert len(chunk) <= 2200  # chunk_size=2000 + some overlap tolerance


def test_load_document_missing_file():
    with pytest.raises(FileNotFoundError):
        load_document("nonexistent_file.txt")


def test_load_document_unsupported_type():
    with pytest.raises(ValueError):
        load_document("file.csv")
