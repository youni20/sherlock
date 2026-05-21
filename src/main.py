from agent import ask_question

def main() -> None:
    question: str = input()
    answer: str = ask_question(question)
    print(answer)

if __name__ == "__main__":
    main()
