from dotenv import load_dotenv
load_dotenv()

from embedding import retrive_context
from vector_store import vector_store

context = retrive_context(vector_store, "What did the night watchman see?")
print(context)

all_chunks = vector_store.get()
print(f"Total chunks in store: {len(all_chunks['ids'])}")
for doc in all_chunks['documents']:
    print(doc[:80])
    print("---")

