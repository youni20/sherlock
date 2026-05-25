from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

from ingestion import DATA_COLLECTION 

import uvicorn

app: FastAPI = FastAPI()

@app.get("/", response_class=FileResponse)
def home() -> FileResponse:
    return FileResponse("src/static/index.html")

@app.get("/get_question")
def get_question(question: str) -> str:
    print(question)
    return(f"Question: {question}")


@app.post("/ingest_file")
async def upload_file(file: UploadFile = File(...)):
    with open(f"{DATA_COLLECTION}/{file.filename}", "wb") as f:
        content = await file.read()
        f.write(content)
        print("Added File")
    return{
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_at": DATA_COLLECTION
    }


if __name__ == "__main__":
    uvicorn.run(app='main:app', port=8080, reload=True)
    # bootstrap_knowledge_base()
    # run_cli()
