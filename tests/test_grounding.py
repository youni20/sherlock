import pytest
from langchain_chroma import Chroma

from generation import ask_question
from ingestion import load_document, split_text
from retrieval import get_embedding_model, retrieve_context


# Every test here drives the real Gemini API — opt-in only.
pytestmark = pytest.mark.integration

#  Exact sentence when evidence is mising
ABSTENTION: str = "I don't have enough evidence to answer that."

CASE_FILES: list[str] = [
    "case_001_thornfield_manor.txt",
    "case_002_finch_disappearance.txt",
    "case_003_blackwood_estate.pdf",
]

#  Isolated in-memory store so the test session never touches the real persistent vector store.
#  Built inside a fixture (not at import) so collecting this file never constructs a real client.
@pytest.fixture(scope="session")
def test_store() -> Chroma:
    store = Chroma(collection_name="test-case-files", embedding_function=get_embedding_model())
    for file in CASE_FILES:  # Ingest all three case files once before the test session
        text = load_document(file)
        chunks = split_text(text)
        store.add_texts(chunks)
    return store


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


ABSTENTION_CASES = [
    "Did the butler have a motive?",
    "Who had a key to the study drawer?",
    "Who started the fire at the Blackwood Estate?",
    "Who poisoned the wine at the dinner party?",
]


@pytest.mark.parametrize("question, keywords", ANSWERABLE_CASES)
def test_answerable_questions(test_store, question, keywords):
    """The answer must contain every expected keyword (case-insensitive)."""
    context = retrieve_context(test_store, question)
    answer = ask_question(question, context)
    lowered = answer.lower()
    for keyword in keywords:
        assert keyword.lower() in lowered, (
            f"Expected '{keyword}' in answer to '{question}'.\n"
            f"Got: {answer!r}"
        )


@pytest.mark.parametrize("question, keywords", ANSWERABLE_CASES)
def test_answerable_questions_do_not_abstain(test_store, question, keywords):
    """Answerable questions must not trigger the abstention response."""
    context = retrieve_context(test_store, question)
    answer = ask_question(question, context)
    assert ABSTENTION not in answer, (
        f"Expected a real answer but got abstention for '{question}'.\n"
        f"Got: {answer!r}"
    )


@pytest.mark.parametrize("question", ABSTENTION_CASES)
def test_abstention_questions(test_store, question):
    """When evidence is absent the system must return the exact abstention sentence."""
    context = retrieve_context(test_store, question)
    answer = ask_question(question, context)
    assert answer.strip() == ABSTENTION, (
        f"Expected the exact abstention sentence for '{question}'.\n"
        f"Expected: {ABSTENTION!r}\n"
        f"Got:      {answer!r}"
    )
