from agent import ask_question
from pathlib import Path

DATA_COLLECTION = Path("case_files")

def main() -> None:
    question: str = input("Question: ")
    answer: str = ask_question(question)
    print(answer)

if __name__ == "__main__":
    main()
