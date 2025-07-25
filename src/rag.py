import warnings
import re
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.tools.tavily_search import TavilySearchResults
from src import config  # Centralized config

# Suppress FAISS deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ✅ Check if query is medically relevant
def is_medical_query(query: str) -> bool:
    medical_keywords = [
        "pain", "symptom", "cough", "headache", "disease", "treatment", "diagnosis",
        "medicine", "health", "fever", "infection", "cancer", "diabetes", "blood",
        "prescription", "clinic", "hospital", "mental health", "anxiety", "therapy",
        "flu", "cold", "rash", "vomiting", "surgery", "injury", "doctor", "nurse",
        "aids", "hiv", "hepatitis", "std", "immunodeficiency", "virus"
    ]
    query = query.lower()
    return any(keyword in query for keyword in medical_keywords)

#  Detect small talk / greetings using regex (fixes 'hi' in 'hiv')
def is_small_talk(query: str) -> bool:
    small_talk_patterns = [
        r"\bhi\b", r"\bhello\b", r"\bhey\b", r"\bhow are you\b",
        r"\bwhat can you do\b", r"\bwho are you\b", r"\bhelp\b",
        r"\bhow can you help\b", r"\bhow does this work\b",
        r"\bwhat is your name\b", r"\bstart\b", r"\bget started\b",
        r"\bintroduce yourself\b"
    ]
    query = query.lower()
    return any(re.search(pattern, query) for pattern in small_talk_patterns)

#  Friendly replies for small talk
def handle_small_talk(query: str) -> str:
    responses = {
        "hi": "Hi there! 👋 How can I help you with your health today?",
        "hello": "Hello! 😊 I'm here to help with medical or health-related questions.",
        "how are you": "I'm doing well, thanks! How can I assist you with your health?",
        "what can you do": "I can help you understand symptoms, suggest general remedies, and provide health advice. 💊",
        "who are you": "I'm your friendly health assistant — ready to guide you with medical questions!",
        "how can you help": "Ask me anything related to your health — symptoms, medicines, or general advice!",
    }
    query = query.lower()
    for key, response in responses.items():
        if key in query:
            return response
    return "I'm here to support you with anything related to health or medical concerns. How can I help you today?"

#  Load and split documents
def load_documents(file_path: str = config.DOC_PATH):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]

#  Create FAISS vector store
def create_vector_store(docs):
    embeddings = GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        google_api_key=config.GEMINI_API_KEY
    )
    return FAISS.from_documents(docs, embeddings)

# RAG pipeline combining FAISS + Tavily
def run_rag(query: str, vector_store):
    query = query.strip()

    # Step 0: Handle small talk
    if is_small_talk(query):
        return handle_small_talk(query)

    # Step 1: Ensure it's a medical query
    if not is_medical_query(query):
        return " I'm here to assist only with health or medical-related topics. Please ask a health-related question."

    # Step 2: Retrieve from FAISS
    retriever = vector_store.as_retriever()
    retrieved_docs = retriever.get_relevant_documents(query)

    if not retrieved_docs:
        print(" No relevant documents found in FAISS.")
    else:
        print(f" Retrieved {len(retrieved_docs)} documents from FAISS.")

    # Step 3: Tavily web search (always run)
    tavily = TavilySearchResults(k=3)
    web_results = tavily.run(query)

    if not web_results:
        print(" Tavily returned no web results.")
    else:
        print(f" Tavily returned {len(web_results)} web results.")

    # Step 4: Convert web results into document
    web_doc = None
    if web_results:
        web_content = "\n".join(
            [f"- {res['content']}" for res in web_results if 'content' in res and res['content']]
        )
        if web_content.strip():
            web_doc = Document(page_content=web_content, metadata={"source": "Tavily"})

    # Step 5: Combine all sources
    combined_docs = []
    sources = []

    if retrieved_docs:
        combined_docs.extend(retrieved_docs)
        sources.append("Local Documents")

    if web_doc:
        combined_docs.append(web_doc)
        sources.append("Web (Tavily)")

    if not combined_docs:
        return " Sorry, I couldn't find any relevant information in local documents or on the web."

    # Step 6: Create system prompt
    system_prompt = f"""
You are a helpful health assistant. Based on the provided documents, answer the user's medical question.
Use both internal content and live web search results where relevant. Be detailed, accurate, and explain step-by-step if needed.

User Query: {query}
"""

    # Step 7: LLM call with chain
    llm = ChatGoogleGenerativeAI(
        model=config.CHAT_MODEL,
        google_api_key=config.GEMINI_API_KEY,
        temperature=0.3,
        convert_system_message_to_human=True,
        model_kwargs={"system_instruction": config.SYSTEM_INSTRUCTION}
    )

    chain = load_qa_chain(llm, chain_type="stuff")
    result = chain.run(
        input_documents=combined_docs,
        question=system_prompt
    )

    return f"Sources used: {', '.join(sources)}\n\n{result}"
