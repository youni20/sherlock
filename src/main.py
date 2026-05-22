from agent import ask_question
from embedding import build_vector_store, retrive_context
from chunk import split_text
from ingest import load_document, DATA_COLLECTION
from dotenv import load_dotenv
import os


def main() -> None:
    load_dotenv()
    all_chunkz: list[str] = []
    for root, dir, files in os.walk(DATA_COLLECTION):  # Iterate through all files in a directory including in sub-directories
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), DATA_COLLECTION)
            text = load_document(file_path)
            chunks_list = split_text(document=text)
            all_chunkz.extend(chunks_list)
            
    vector_store = build_vector_store(chunks=all_chunkz)
    
    # print(f"Character count: {len(text)}")

    question: str = input("Question: ")
    docs: str = retrive_context(vector_store=vector_store, question=question)
    answer: str = ask_question(question, docs)
    print(answer)

    
if __name__ == "__main__":
    main()