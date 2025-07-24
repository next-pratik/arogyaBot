from src.rag import load_documents, create_vector_store, run_rag
from src import config  # ✅ centralized config

def run_query(query: str) -> str:
    docs = load_documents(config.DOC_PATH)  # ✅ use configured path
    vector_store = create_vector_store(docs)
    return run_rag(query, vector_store)

if __name__ == '__main__':
    q = input("Ask ArogyaBot: ")
    print(run_query(q))
