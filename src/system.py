from dotenv import load_dotenv
load_dotenv()

from generation import ask_question
from retrieval import retrieve_context, vector_store, retrieve_context_with_sources
from ingestion import split_text, load_document, DATA_COLLECTION

import hashlib
import os


def embed_file(file_name: str) -> None:  # Embed a single file's chunks into the store
    text = load_document(file_name)
    chunks = split_text(document=text)
    ids = [hashlib.sha256(c.encode()).hexdigest() for c in chunks]  # Same chunk content -> same hash -> Chroma deduplicates on insert
    source = os.path.basename(file_name)  # Tag each chunk with the filename it came from
    vector_store.add_texts(chunks, metadatas=[{"source": source}] * len(chunks), ids=ids)


# Utility to re-embed every file in the collection (e.g. after wiping the vector store).
# Not used by the upload flow, which embeds only the newly added file via embed_file().
# def bootstrap_knowledge_base() -> None:
#     for root, dirs, files in os.walk(DATA_COLLECTION):  # Iterate through all files including sub-directories
#         for file in files:
#             embed_file(os.path.relpath(os.path.join(root, file), DATA_COLLECTION))


def run_cli() -> None:
    running: bool = True

    while(running):
        question: str = input("Question: ")
        if (question == "/exit"):
            running = False
            break
        #  docs: str = retrieve_context(vector_store=vector_store, question=question)
        docs, sources = retrieve_context_with_sources(vector_store=vector_store, question=question)
        answer: str = ask_question(question, docs)
        print(f"response: {answer}")
        print(f"sources: {sources}")
