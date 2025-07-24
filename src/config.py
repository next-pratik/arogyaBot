import os
from dotenv import load_dotenv

# ✅ Load from .env once when config is imported
load_dotenv()

# 🔐 API KEYS
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# 📄 DATA SETTINGS
DOC_PATH = "data/medical_docs.txt"

# 🧠 MODEL CONFIG
EMBEDDING_MODEL = "models/embedding-001"
CHAT_MODEL = "gemini-1.5-flash"  # or gemini-1.5-pro-latest

# 🤖 SYSTEM PROMPT (customized per use case)
SYSTEM_INSTRUCTION = (
    "You are a helpful medical assistant. Only answer questions related to health and medicine. "
    "If the question is unrelated, respond with: "
    "'I'm here to help only with medical-related topics.'"
)
