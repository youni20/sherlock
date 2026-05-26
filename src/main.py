from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

from retrieval import retrieve_context_with_sources, vector_store
from system import bootstrap_knowledge_base
from ingestion import DATA_COLLECTION
from generation import ask_question

import uvicorn
import shutil


VECTOR_STORE: Path = Path("./chroma_vector_store")

class QuestionRequest(BaseModel):
    question: str

app: FastAPI = FastAPI()

@app.get("/", response_class=FileResponse)
def home() -> FileResponse:
    return FileResponse("src/static/index.html")

@app.post("/ingest_file")
async def upload_file(file: UploadFile = File(...)):
    with open(f"{DATA_COLLECTION}/{file.filename}", "wb") as f:
        content = await file.read()
        f.write(content)
        print("Added File")

    bootstrap_knowledge_base()
    print("Embedded File")
    
    return{
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_at": DATA_COLLECTION
    }

@app.post("/get_answer")
def get_answer(body: QuestionRequest) -> dict:
    docs, sources = retrieve_context_with_sources(vector_store=vector_store, question=body.question)
    answer: str = ask_question(body.question, docs)
    return {"answer": answer, "sources": sources}

@app.delete("/delete_files")
def remove_files() -> None:
    for file in DATA_COLLECTION.rglob("*"):
        if file.is_file():
            file.unlink()
    vector_store.reset_collection()
    shutil.rmtree(VECTOR_STORE)
    VECTOR_STORE.mkdir()
    print("All files and embeddings deleted")

@app.get("/get_files")
def get_files() -> list[str]:
    case_files: list[str] = [] 
    for file in DATA_COLLECTION.rglob("*"):
        if file.is_file():
            case_files.append(file.name)
    return case_files
        

if __name__ == "__main__":
    uvicorn.run(app='main:app', port=8080, reload=True)