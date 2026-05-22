from langchain_core.documents.base import Document
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

#  Initialise the embedding model
embedding_model = OllamaEmbeddings(
    model="embeddinggemma:latest",
    dimensions=768
)

#  Define method to store the chunks (for now in memory ill make a dir for it later)
def store_vector(text: list[str], question: str):
    vector_store = InMemoryVectorStore.from_texts(text, embedding=embedding_model)
    retriever: VectorStoreRetriever = vector_store.as_retriever()
    retrived_documents: list[Document] = retriever.invoke(question)

    return retrived_documents[0].page_content
    