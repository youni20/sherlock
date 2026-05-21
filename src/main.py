from agent import ask_question
from ingest import load_document

def main() -> None:
    text = load_document("test.txt")
    print(f"Character count: {len(text)}")
    print(text)

    question: str = input("Question: ")
    answer: str = ask_question(question)
    print(answer)

if __name__ == "__main__":
    main()
