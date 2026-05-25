from fastapi import FastAPI
from fastapi.responses import FileResponse

import uvicorn

app: FastAPI = FastAPI()

@app.get("/", response_class=FileResponse)
def home() -> FileResponse:
    return FileResponse("src/static/index.html")

@app.get("/get_question")
def get_question(question: str) -> str:
    print(question)
    return(f"Question: {question}")

if __name__ == "__main__":
    uvicorn.run(app='main:app', port=8080, reload=True)
    # bootstrap_knowledge_base()
    # run_cli()
