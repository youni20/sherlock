from dotenv import load_dotenv
load_dotenv()

from generation import ask_question
from retrival import retrive_context, vector_store
from ingestion import split_text, load_document, DATA_COLLECTION

import hashlib
import os


def run_system() -> None:
    if not vector_store.get()['ids']:  # To avoid rembedding anything thats already embedded
        all_chunkz: list[str] = []
        for root, dir, files in os.walk(DATA_COLLECTION):  # Iterate through all files in a directory including in sub-directories
            for file in files:
                file_path = os.path.relpath(os.path.join(root, file), DATA_COLLECTION)
                text = load_document(file_path)
                chunks_list = split_text(document=text)
                all_chunkz.extend(chunks_list)
            
        ids: list[str] = [hashlib.sha256(c.encode()).hexdigest() for c in all_chunkz]  # Hash function where same input always gives same output
        vector_store.add_texts(all_chunkz, ids=ids)

    running: bool = True

    while(running):
        question: str = input("Question: ")
        if (question == "/exit"):
            running = False
            break
        docs: str = retrive_context(vector_store=vector_store, question=question)
        answer: str = ask_question(question, docs)
        print(answer)
