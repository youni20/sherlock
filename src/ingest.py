from pypdf import PdfReader
from pathlib import Path

DATA_COLLECTION: Path = Path("case_files")

def load_document(file_name: str) -> str:
    file_path: Path = DATA_COLLECTION / file_name

    if not file_path.exists():
        raise FileNotFoundError("Error invalid file path")
        
    if file_name.endswith(".pdf"):
        try:
            reader: PdfReader = PdfReader(file_path)
            text: str = ""
            for page in reader.pages:
                text = text + page.extract_text()
        except Exception as e:
            raise RuntimeError(f"Failed to parse PDF: {file_name}") from e
        return text
            
    if file_name.endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file_content: str = file.read()
                return file_content
        except Exception as e:
            raise RuntimeError(f"Failed to read text file: {file_name}") from e

    raise ValueError(f"Unsupported file type: {file_name}. Expected .pdf or .txt")