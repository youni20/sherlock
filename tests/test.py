import pytest

from agent import ask_question
from ingest import load_document
from chunker import split_text
from vector_store import vector_store
from embedding import retrive_context

#  Exact sentence when evidence is mising
ABSTENTION: str = "I don't have enough evidence to answer that."

CASE_FILES: list[str] = [
    "txt_files/case_001_thornfield_manor.txt",
    "txt_files/case_002_finch_disappearance.txt",
    "pdf_files/case_003_blackwood_estate.pdf",
]

@pytest.fixture(scope="session", autouse=True)
def knowledge_base():  # Ingest all three case files once before the test session
    for file in CASE_FILES:
        text = load_document(file)
        chunks = split_text(text)
        vector_store.add_texts(chunks)


#  Questions that should be answerable and based of case 001
#  Each case is a (question, [keywords that must ALL appear in the answer])
ANSWERABLE_CASES = [
    (
        "What was Mrs. Hudson's alibi?",
        ["kitchen", "midnight"],
    ),
    (
        "Who was seen leaving the manor at midnight?",
        ["Sykes"],
    ),
    (
        "What was stolen from Thornfield Manor?",
        ["necklace"],
    ),
    (
        "What time did the butler bolt the doors?",
        ["half past ten"],
    ),
    # Answerable: case 003, the Blackwood arson PDF
    (
        "Why was Tom Reeve dismissed from the Blackwood Estate?",
        ["theft"],
    ),
    (
        "What did the night watchman see?",
        ["man"],   # a man in a dark coat heading for the south gate
    ),
    # Answerable: case 002, the Finch disappearance (cross-document retrieval)
    (
        "What happened to Albert Finch?",
        ["Finch"],
    ),
]


@pytest.mark.parametrize("question, keywords", ANSWERABLE_CASES)
def test_answerable_questions(question, keywords):
    """The answer must contain every expected keyword (case-insensitive)."""
    context = retrive_context(vector_store, question)
    answer = ask_question(question, context)
    lowered = answer.lower()
    for keyword in keywords:
        assert keyword.lower() in lowered, (
            f"Expected '{keyword}' in answer to '{question}'.\n"
            f"Got: {answer!r}"
        )
