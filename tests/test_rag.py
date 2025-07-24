from src import rag

def test_load_documents():
    docs = rag.load_documents("data/medical_docs.txt")
    assert len(docs) > 0
    assert hasattr(docs[0], "page_content")

def test_create_vector_store():
    docs = rag.load_documents("data/medical_docs.txt")
    store = rag.create_vector_store(docs)
    assert store is not None

def test_run_rag_basic():
    docs = rag.load_documents("data/medical_docs.txt")
    store = rag.create_vector_store(docs)
    response = rag.run_rag("What causes headaches?", store)
    assert isinstance(response, str)
    assert len(response) > 0
