from agent import ask_question
from embedding import build_vector_store, retrive_context
from chunk import split_text
from ingest import load_document, DATA_COLLECTION
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    text = load_document("test.txt")
    chunks_list = split_text(document=text)
    vector_store = build_vector_store(chunks=chunks_list)
    
    # print(f"Character count: {len(text)}")

    question: str = input("Question: ")
    docs: str = retrive_context(vector_store=vector_store, question=question)
    answer: str = ask_question(question, docs)
    print(answer)


    
if __name__ == "__main__":
    main()
