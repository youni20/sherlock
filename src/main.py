from agent import ask_question
from embedding import build_vector_store, retrive_context
from chunk import split_text
from ingest import load_document, DATA_COLLECTION
from dotenv import load_dotenv
import os


def main() -> None:
    load_dotenv()
    for root, dir, files in os.walk(DATA_COLLECTION):
        for file in files:
            text = load_document(file)
            chunks_list = split_text(document=text)
            vector_store = build_vector_store(chunks=chunks_list)
    
    # print(f"Character count: {len(text)}")

    question: str = input("Question: ")
    docs: str = retrive_context(vector_store=vector_store, question=question)
    answer: str = ask_question(question, docs)
    print(answer)

    
if __name__ == "__main__":
    main()