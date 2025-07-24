import warnings
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.tools.tavily_search import TavilySearchResults
from src import config  # Centralized config

# Suppress FAISS deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ✅ Utility: Check if query is medical
def is_medical_query(query: str) -> bool:
    medical_keywords = [
        "pain", "symptom", "cough", "headache", "disease", "treatment", "diagnosis",
        "medicine", "health", "fever", "infection", "cancer", "diabetes", "blood",
        "prescription", "clinic", "hospital", "mental health", "anxiety", "therapy",
        "flu", "cold", "rash", "vomiting", "surgery", "injury", "doctor", "nurse"
    ]
    query = query.lower()
    return any(keyword in query for keyword in medical_keywords)

# ✅ Load and split documents into chunks
def load_documents(file_path: str = config.DOC_PATH):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]

# ✅ Create FAISS vector store using Gemini embeddings
def create_vector_store(docs):
    embeddings = GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        google_api_key=config.GEMINI_API_KEY
    )
    return FAISS.from_documents(docs, embeddings)

# ✅ Run RAG pipeline
def run_rag(query: str, vector_store):
    # Step 0: Validate medical relevance
    if not is_medical_query(query):
        return "⚠️ I'm here to assist only with health or medical-related topics. Please ask a health-related question."

    # Step 1: Retrieve local chunks
    retriever = vector_store.as_retriever()
    retrieved_docs = retriever.get_relevant_documents(query)

    # Step 2: Search web with Tavily
    tavily = TavilySearchResults(k=3)
    web_results = tavily.run(query)

    # Step 3: Combine sources
    combined_docs = []

    if retrieved_docs:
        combined_docs.extend(retrieved_docs)

    if web_results:
        web_content = "\n".join([f"- {res['content']}" for res in web_results])
        web_doc = Document(page_content=web_content, metadata={"source": "Tavily"})
        combined_docs.append(web_doc)

    # Step 4: Generate answer using Gemini
    llm = ChatGoogleGenerativeAI(
        model=config.CHAT_MODEL,
        google_api_key=config.GEMINI_API_KEY,
        temperature=0.3,
        convert_system_message_to_human=True,
        model_kwargs={"system_instruction": config.SYSTEM_INSTRUCTION}
    )

    chain = load_qa_chain(llm, chain_type="stuff")
    result = chain.run(input_documents=combined_docs, question=query)

    return result
