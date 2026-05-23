import pytest

from src.agent import ask_question
from src.ingest import load_document

#  Exact sentence when evidence is mising
ABSTENTION: str = "I don't have enough evidence to answer that."

CASE_FILES: list = [
    "case_files/case_001_thornfield_manor.txt",
    "case_files/case_002_finch_disappearance.txt",
    "case_files/case_003_blackwood_estate.pdf",
]
