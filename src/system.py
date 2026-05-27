from dotenv import load_dotenv
load_dotenv()

from retrieval import get_vector_store
from ingestion import split_text, load_document

import hashlib
import os


def embed_file(file_name: str) -> None:  # Embed a single file's chunks into the store
    text = load_document(file_name)
    chunks = split_text(document=text)
    ids = [hashlib.sha256(c.encode()).hexdigest() for c in chunks]  # Same chunk content -> same hash -> Chroma deduplicates on insert
    source = os.path.basename(file_name)  # Tag each chunk with the filename it came from
    get_vector_store().add_texts(chunks, metadatas=[{"source": source}] * len(chunks), ids=ids)
