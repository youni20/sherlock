from dotenv import load_dotenv
load_dotenv()

from generation import ask_question
from retrieval import retrive_context, vector_store
from ingestion import split_text, load_document, DATA_COLLECTION

import hashlib
import os


def bootstrap_knowledge_base() -> None:  # Embeds whatever hasnt been embedded yet
    all_chunkz: list[str] = []
    all_metadatas: list[dict] = []
    for root, dir, files in os.walk(DATA_COLLECTION):  # Iterate through all files in a directory including in sub-directories
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), DATA_COLLECTION)
            text = load_document(file_path)
            chunks_list = split_text(document=text)
            all_chunkz.extend(chunks_list)
            all_metadatas.extend([{"source": file}] * len(chunks_list))  # Tag each chunk with the filename it came from

    ids: list[str] = [hashlib.sha256(c.encode()).hexdigest() for c in all_chunkz]  # Same chunk content -> same hash -> Chroma deduplicates on update and insert
    vector_store.add_texts(all_chunkz, metadatas=all_metadatas, ids=ids)


def run_cli() -> None:
    running: bool = True

    while(running):
        question: str = input("Question: ")
        if (question == "/exit"):
            running = False
            break
        docs: str = retrive_context(vector_store=vector_store, question=question)
        answer: str = ask_question(question, docs)
        print(answer)
