import pytest

from src.agent import ask_question
from src.ingest import load_document

#  Exact sentence when evidence is mising
ABSTENTION: str = "I don't have enough evidence to answer that."

CASE_FILES: list[str] = [
    "case_files/case_001_thornfield_manor.txt",
    "case_files/case_002_finch_disappearance.txt",
    "case_files/case_003_blackwood_estate.pdf",
]

@pytest.fixture(scope="session", autouse=True)
def knowledge_base():  # Ingest all three case files once before the test session
    for file in CASE_FILES:
        load_document(file)


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

