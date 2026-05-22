from langchain_ollama import OllamaEmbeddings

embedding_model = OllamaEmbeddings(
    model="embeddinggemma:latest",
    dimensions=768
)