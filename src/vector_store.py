from langchain_chroma import Chroma
from embedding import embedding_model

vector_store = Chroma(
    collection_name="case-files",
    embedding_function=embedding_model,
    persist_directory="./chroma_vector_store"
)