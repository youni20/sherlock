from pypdf import PageObject, PdfReader
from pathlib import Path

DATA_COLLECTION: Path = Path("case_files")

def load_document(file_name: str) -> str:
    file_path: Path = DATA_COLLECTION / file_name

    if not file_path.exists():
        raise Exception("Error invalid file path")
    try:
        if file_name.endswith(".pdf"):
            reader: PdfReader = PdfReader(file_path)
            page: PageObject = reader.pages[0]
            text: str = page.extract_text()
            # print(text)
            return text
        elif file_name.endswith(".txt"):
             with open(file_path, "r") as file:
                 file_content: str = file.read()
                 return file_content
        else: raise Exception("Error: File is not of type pdf or txt file")
    except:
        raise Exception(f"Error Ingesting Document: {file_name} \n Located In: {file_path}")
        