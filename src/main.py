# src/main.py
import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


from src.rag import load_documents, create_vector_store, run_rag
from src import config

# 🟡 Defer document loading and vector store creation
docs = None
vector_store = None

def init_vector_store():
    global docs, vector_store
    if vector_store is None:
        docs = load_documents(config.DOC_PATH)
        vector_store = create_vector_store(docs)
    return vector_store

# ✅ Main query interface used by Streamlit
def run_query(query: str) -> str:
    try:
        store = init_vector_store()  # <-- lazy load here
        return run_rag(query, store)
    except Exception as e:
        return f"❌ An error occurred while processing your question: {str(e)}"

# ✅ Optional: CLI interface for local testing
if __name__ == '__main__':
    print("🩺 ArogyaBot – Medical Assistant (type 'exit' to quit)")
    while True:
        user_input = input("\n You: ")
        if user_input.strip().lower() == "exit":
            break
        print("\n Bot:", run_query(user_input))
