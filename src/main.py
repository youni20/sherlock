from agent import ask_question
from ingest import load_document

def main() -> None:
    load_document("names.pdf")
"""
    question: str = input("Question: ")
    answer: str = ask_question(question)
    print(answer)
"""

if __name__ == "__main__":
    main()
