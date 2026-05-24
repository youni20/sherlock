from pypdf import PdfReader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_COLLECTION: Path = Path("case_files")


def split_text(document: str) -> list[str]:  # Chunking the text for the embedding model 
    text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    texts: list[str] = text_splitter.split_text(document)
    return texts
    

def load_document(file_name: str) -> str:
    file_path: Path = DATA_COLLECTION / file_name

    if not file_path.exists():
        raise FileNotFoundError("Error invalid file path")
        
    if file_name.endswith(".pdf"):  # If file is a pdf file
        try:
            reader: PdfReader = PdfReader(file_path)
            text: str = ""
            for page in reader.pages:
                text = text + page.extract_text()
        except Exception as e:
            raise RuntimeError(f"Failed to parse PDF: {file_name}") from e
        return text
            
    if file_name.endswith(".txt"):  # If file is a text file
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file_content: str = file.read()
                return file_content
        except Exception as e:
            raise RuntimeError(f"Failed to read text file: {file_name}") from e

    raise ValueError(f"Unsupported file type: {file_name}. Expected .pdf or .txt")