from embedding import retrive_context
from vector_store import vector_store

context = retrive_context(vector_store, "What did the night watchman see?")
print(context)