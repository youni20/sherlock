from agent import ask_question
from embedding import embedding_model, store_vector
from ingest import load_document
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    text = load_document("test.txt")
    # print(f"Character count: {len(text)}")
    vector = embedding_model.embed_query(text=text)

    question = input("Question: ")
    docs = store_vector(text=text, question=question)
    print(docs)
    '''
    question: str = input("Question: ")
    answer: str = ask_question(question)
    print(answer)
    '''


    
if __name__ == "__main__":
    main()
