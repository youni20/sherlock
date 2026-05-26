from dotenv import load_dotenv
load_dotenv()

from retrieval import retrieve_context, vector_store


context = retrieve_context(vector_store, "What did the night watchman see?")
print(context)

all_chunks = vector_store.get()
print(f"Total chunks in store: {len(all_chunks['ids'])}")
for doc, meta in zip(all_chunks['documents'], all_chunks['metadatas']):
    print(f"source: {meta}")
    print(doc[:80])
    print("---")