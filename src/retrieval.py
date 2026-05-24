from langchain_core.documents.base import Document
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_ollama import OllamaEmbeddings
#  from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import VectorStore
from langchain_chroma import Chroma


#  Initialise the embedding model
embedding_model: OllamaEmbeddings = OllamaEmbeddings(
    model="embeddinggemma"
    # output_dimensionality=768,
)

vector_store: Chroma = Chroma(
    collection_name="case-files",
    embedding_function=embedding_model,
    persist_directory="./chroma_vector_store"
)

def retrive_context(vector_store: VectorStore, question: str) -> str:
    retriever: VectorStoreRetriever = vector_store.as_retriever()
    retrieved_documents: list[Document] = retriever.invoke(question)
    chunks: list[str] = []
    for doc in retrieved_documents:
        chunks.append(doc.page_content)

    return "\n\n".join(chunks)



