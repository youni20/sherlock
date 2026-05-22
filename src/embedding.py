from langchain_core.documents.base import Document
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import VectorStore

#  Initialise the embedding model
embedding_model: OllamaEmbeddings = OllamaEmbeddings(
    model="embeddinggemma:latest",
    dimensions=768
)

def retrive_context(vector_store: VectorStore, question: str) -> str:
    retriever: VectorStoreRetriever = vector_store.as_retriever()
    retrieved_documents: list[Document] = retriever.invoke(question)
    chunks: list[str] = []
    for doc in retrieved_documents:
        chunks.append(doc.page_content)

    return "\n\n".join(chunks)



'''
#  No longer needed as we got persisitent storage with chroma db now
#  Split store vector into 2 functions one to store it and one to query it 
def build_vector_store(chunks: list[str]) -> InMemoryVectorStore:
    return InMemoryVectorStore.from_texts(chunks, embedding=embedding_model)
'''    

'''
#  Define method to store the chunks (for now in memory ill make a dir for it later)
def store_vector(text: list[str], question: str):
    vector_store = InMemoryVectorStore.from_texts(text, embedding=embedding_model)
    retriever: VectorStoreRetriever = vector_store.as_retriever()
    retrived_documents: list[Document] = retriever.invoke(question)

    return retrived_documents[0].page_content
'''