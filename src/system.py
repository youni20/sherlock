from dotenv import load_dotenv
load_dotenv()

from generation import ask_question
from retrieval import vector_store, retrieve_context_with_sources
from ingestion import split_text, load_document, DATA_COLLECTION

import hashlib
import os


def embed_file(file_name: str) -> None:  # Embed a single file's chunks into the store
    text = load_document(file_name)
    chunks = split_text(document=text)
    ids = [hashlib.sha256(c.encode()).hexdigest() for c in chunks]  # Same chunk content -> same hash -> Chroma deduplicates on insert
    source = os.path.basename(file_name)  # Tag each chunk with the filename it came from
    vector_store.add_texts(chunks, metadatas=[{"source": source}] * len(chunks), ids=ids)


def run_cli() -> None:
    while True:
        question: str = input("Question: ")
        if question == "/exit":
            break
        docs, sources = retrieve_context_with_sources(vector_store=vector_store, question=question)
        answer: str = ask_question(question, docs)
        print(f"response: {answer}")
        print(f"sources: {sources}")
