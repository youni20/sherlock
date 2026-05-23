from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(document: str) -> list[str]:  # Chunking the text for the embedding model 
    text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    texts: list[str] = text_splitter.split_text(document)
    return texts