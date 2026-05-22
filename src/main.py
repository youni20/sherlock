from agent import ask_question
from embedding import embedding_model, store_vector
from chunk import split_text
from ingest import load_document, DATA_COLLECTION
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    text = load_document("test.txt")
    chunks_list = split_text(text)
    
    # print(f"Character count: {len(text)}")

    question: str = input("Question: ")
    docs: str = store_vector(text=chunks_list, question=question)
    answer: str = ask_question(question, docs)
    print(answer)


    
if __name__ == "__main__":
    main()
