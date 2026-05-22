from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(document: str) -> list[str]:
    text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    texts: list[str] = text_splitter.split_text(document)
    return texts