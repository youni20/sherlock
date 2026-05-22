from agent import ask_question
from embedding import embedding_model, store_vector
from chunk import split_text
from ingest import load_document, DATA_COLLECTION
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    text = load_document("test.txt")
    splitup = split_text(text)
    print(splitup[0])
    

    '''
    # print(f"Character count: {len(text)}")
    vector = embedding_model.embed_query(text=text)

    question = input("Question: ")
    docs = store_vector(text=text, question=question)
    print(docs)
    
    question: str = input("Question: ")
    answer: str = ask_question(question)
    print(answer)
    '''


    
if __name__ == "__main__":
    main()
