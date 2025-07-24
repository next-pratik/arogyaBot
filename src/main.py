from src.rag import load_documents, create_vector_store, run_rag
from src import config

# 🧠 Load once at start
docs = load_documents(config.DOC_PATH)
vector_store = create_vector_store(docs)

def run_query(query: str) -> str:
    return run_rag(query, vector_store)

if __name__ == '__main__':
    while True:
        q = input("Ask ArogyaBot (or type 'exit'): ")
        if q.lower() == 'exit':
            break
        print("\n🧠 Answer:\n", run_query(q))
