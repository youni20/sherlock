from agent import ask_question
from embedding import embedding_model
from ingest import load_document
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    text = load_document("test.txt")
    print(f"Character count: {len(text)}")
    print(text)

    question: str = input("Question: ")
    answer: str = ask_question(question)
    print(answer)
    
    vector_test = embedding_model.embed_query(text=text)
    print(vector_test)

    
if __name__ == "__main__":
    main()
