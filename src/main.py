from doctest import debug

from system import bootstrap_knowledge_base, run_cli
from fastapi import FastAPI
import uvicorn

app: FastAPI = FastAPI()

@app.get("/")
def home() -> str:
    return "Home Page"


if __name__ == "__main__":
    uvicorn.run(app='main:app', port=8080, reload=True)
    # bootstrap_knowledge_base()
    # run_cli()