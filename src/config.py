import os
from dotenv import load_dotenv

#Load from .env once when config is imported
load_dotenv()

#API KEYS
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

#DATA SETTINGS
DOC_PATH = "data/medical_docs.txt"

#  MODEL CONFIG
EMBEDDING_MODEL = "models/embedding-001"
CHAT_MODEL = "gemini-1.5-flash"  # or gemini-1.5-pro-latest

#  SYSTEM PROMPT (customized per use case)
SYSTEM_INSTRUCTION = (
    "You are a helpful and detailed medical assistant. Provide comprehensive, clear, and user-friendly explanations for medical questions. "
    "Always include treatments, causes, when to see a doctor, and lifestyle tips if relevant. "
    "Use bullet points or short paragraphs to improve readability."
)

