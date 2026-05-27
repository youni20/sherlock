from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from retrieval import retrieve_context_with_sources, get_vector_store
from system import embed_file
from ingestion import DATA_COLLECTION
from generation import ask_question

import uvicorn
import re


class QuestionRequest(BaseModel):
    question: str

app: FastAPI = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.get("/", response_class=FileResponse)
def home() -> FileResponse:
    return FileResponse("src/static/index.html")

@app.post("/ingest_file")
async def upload_file(file: UploadFile = File(...)):
    if not (file.filename or "").lower().endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only .pdf and .txt files are supported.")

    with open(f"{DATA_COLLECTION}/{file.filename}", "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        embed_file(file.filename)
    except Exception as e:
        (DATA_COLLECTION / file.filename).unlink(missing_ok=True)  # don't keep a file we couldn't embed
        raise HTTPException(status_code=502, detail=f"Could not process '{file.filename}'. The file was not added.") from e

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_at": DATA_COLLECTION
    }

@app.post("/get_answer")
def get_answer(body: QuestionRequest) -> dict:
    try:
        docs, retrieved_sources = retrieve_context_with_sources(vector_store=get_vector_store(), question=body.question)
        raw: str = ask_question(body.question, docs)
    except Exception as e:
        raise HTTPException(status_code=502, detail="Could not generate an answer right now. Please try again.") from e

    match = re.search(r"^SOURCES:\s*(.*)$", raw, re.MULTILINE)
    if match and match.group(1).strip().lower() != "none":
        cited = [s.strip() for s in match.group(1).split(",") if s.strip()]
        sources = [s for s in cited if s in retrieved_sources]
    else:
        sources = []
    answer = re.sub(r"\n?^SOURCES:.*$", "", raw, flags=re.MULTILINE).strip()

    return {"answer": answer, "sources": sources}

@app.delete("/delete_files")
def remove_files() -> None:
    for file in DATA_COLLECTION.rglob("*"):
        if file.is_file():
            file.unlink()
    get_vector_store().reset_collection()

@app.get("/get_files")
def get_files() -> list[str]:
    case_files: list[str] = []
    for file in DATA_COLLECTION.rglob("*"):
        if file.is_file():
            case_files.append(file.name)
    return case_files


if __name__ == "__main__":
    uvicorn.run(app='main:app', port=8080, reload=True)