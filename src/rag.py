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
        "flu", "cold", "rash", "vomiting", "surgery", "injury", "doctor", "nurse",
        "aids", "hiv", "hepatitis", "std", "immunodeficiency", "virus"
    ]
    query = query.lower()
    return any(keyword in query for keyword in medical_keywords)

# ✅ Utility: Detect small talk / greetings
def is_small_talk(query: str) -> bool:
    small_talk_phrases = [
        "hi", "hello", "hey", "how are you", "what can you do", "who are you",
        "help", "how can you help", "how does this work", "what is your name",
        "start", "get started", "introduce yourself"
    ]
    query = query.lower()
    return any(phrase in query for phrase in small_talk_phrases)

# ✅ Utility: Friendly small talk replies
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

# ✅ Load and split documents into chunks
def load_documents(file_path: str = config.DOC_PATH):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]

# ✅ Create FAISS vector store using Gemini embeddings
def create_vector_store(docs):
    embeddings = GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        google_api_key=config.GEMINI_API_KEY
    )
    return FAISS.from_documents(docs, embeddings)

# ✅ Run RAG pipeline with web and doc fallback
def run_rag(query: str, vector_store):
    query = query.strip()

    # Step 0: Handle greetings and general small talk
    if is_small_talk(query):
        return handle_small_talk(query)

    # Step 1: Validate medical relevance
    if not is_medical_query(query):
        return "⚠️ I'm here to assist only with health or medical-related topics. Please ask a health-related question."

    # Step 2: Retrieve from local documents (FAISS)
    retriever = vector_store.as_retriever()
    retrieved_docs = retriever.get_relevant_documents(query)

    if not retrieved_docs:
        print("⚠️ No relevant documents found in FAISS.")
    else:
        print(f"✅ Retrieved {len(retrieved_docs)} documents from FAISS.")

    # Step 3: Search web with Tavily
    tavily = TavilySearchResults(k=3)
    web_results = tavily.run(query)

    if not web_results:
        print("⚠️ Tavily returned no web results.")
    else:
        print(f"🌐 Tavily returned {len(web_results)} web results.")

    # Step 4: Convert Tavily results into a document
    web_content = ""
    if web_results:
        web_content = "\n".join(
            [f"- {res['content']}" for res in web_results if 'content' in res and res['content']]
        )

    web_doc = Document(page_content=web_content, metadata={"source": "Tavily"}) if web_content else None

    # Step 5: Combine retrieved docs and web docs
    combined_docs = []
    sources = []

    if retrieved_docs:
        combined_docs.extend(retrieved_docs)
        sources.append("📚 Local Documents")

    if web_doc:
        combined_docs.append(web_doc)
        sources.append("🌐 Web (Tavily)")

    if not combined_docs:
        return "❌ Sorry, I couldn't find any relevant information in local documents or on the web."

    # Step 6: System prompt
    system_prompt = f"""
You are a helpful health assistant. Based on the provided documents, answer the user's medical question.
Use both internal content and live web search results where relevant. Be detailed, accurate, and explain step-by-step if needed.

User Query: {query}
"""

    # Step 7: Run LLM with chain
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

    return f"🔍 Sources used: {', '.join(sources)}\n\n{result}"
