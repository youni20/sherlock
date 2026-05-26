from langchain_core.documents.base import Document
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import VectorStore
from langchain_chroma import Chroma


#  Initialise the embedding model
embedding_model: GoogleGenerativeAIEmbeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

vector_store: Chroma = Chroma(
    collection_name="case-files",
    embedding_function=embedding_model,
    persist_directory="./chroma_vector_store"
)

def retrieve_context(vector_store: VectorStore, question: str) -> str:
    retriever: VectorStoreRetriever = vector_store.as_retriever()
    retrieved_documents: list[Document] = retriever.invoke(question)
    chunks: list[str] = []
    for doc in retrieved_documents:
        chunks.append(doc.page_content)

    return "\n\n".join(chunks)


def retrieve_context_with_sources(vector_store: VectorStore, question: str) -> tuple[str, list[str]]:
    retriever: VectorStoreRetriever = vector_store.as_retriever()
    retrieved_documents: list[Document] = retriever.invoke(question)
    chunks: list[str] = []
    sources: list[str] = []
    for doc in retrieved_documents:
        src: str = doc.metadata.get("source", "unknown")
        chunks.append(f"[Source: {src}]\n{doc.page_content}")
        sources.append(src)

    return "\n\n".join(chunks), list(dict.fromkeys(sources))
