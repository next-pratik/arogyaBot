import warnings
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter

from src import config  # ✅ import your centralized config

# ✅ Suppress FAISS deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ✅ Load and split documents
def load_documents(file_path: str = config.DOC_PATH):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]

# ✅ Create vector store using Gemini embedding model
def create_vector_store(docs):
    embeddings = GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        google_api_key=config.GEMINI_API_KEY
    )
    return FAISS.from_documents(docs, embeddings)

# ✅ Run Retrieval-Augmented Generation with system prompt
def run_rag(query: str, vector_store):
    retriever = vector_store.as_retriever()
    llm = ChatGoogleGenerativeAI(
        model=config.CHAT_MODEL,
        google_api_key=config.GEMINI_API_KEY,
        temperature=0.3,
        convert_system_message_to_human=True, 
        model_kwargs={"system_instruction": config.SYSTEM_INSTRUCTION}
    )
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )
    result = qa.invoke({"query": query})
    return result['result']
