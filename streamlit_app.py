import asyncio
import sys

if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop(asyncio.new_event_loop())
    except RuntimeError:
        pass

import streamlit as st
from io import BytesIO
from gtts import gTTS
from googletrans import Translator
from src.main import run_query  # Ensure this uses lazy vector store init

# Set Streamlit page config
st.set_page_config(page_title="ArogyaBot – Medical Assistant", layout="centered")

# Custom CSS styling
st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        .chat-message {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 1rem;
            max-width: 85%;
            line-height: 1.6;
        }
        .user {
            background-color: #1f2937;
            align-self: flex-end;
            margin-left: auto;
        }
        .bot {
            background-color: #27272a;
            align-self: flex-start;
            margin-right: auto;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🩺 ArogyaBot – Your Trusted Health Assistant</h1>", unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar with chat history clear
with st.sidebar:
    st.markdown("### 🕓 Chat History")
    if st.button("🧹 Clear"):
        st.session_state.chat_history = []
        st.rerun()

# Display past messages
for chat in st.session_state.chat_history:
    st.markdown(f"<div class='chat-container'><div class='chat-message user'>{chat['user']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-container'><div class='chat-message bot'>{chat['bot']}</div></div>", unsafe_allow_html=True)
    if chat.get("audio"):
        st.audio(chat["audio"], format="audio/mp3")

# Chat input
if prompt := st.chat_input("Ask a medical question in any language..."):
    translator = Translator()

    # Detect language using Google Translate
    detection = translator.detect(prompt)
    lang = detection.lang

    # Translate prompt to English if needed
    translated_prompt = translator.translate(prompt, dest="en").text if lang != "en" else prompt

    st.markdown(f"<div class='chat-container'><div class='chat-message user'>{prompt}</div></div>", unsafe_allow_html=True)

    with st.spinner("Processing..."):
        try:
            # Query the bot
            reply_en = run_query(translated_prompt)

            # Translate reply back to original language
            reply_local = translator.translate(reply_en, dest=lang).text if lang != "en" else reply_en

            # Text-to-Speech
            tts = gTTS(text=reply_local, lang=lang)
            audio_fp = BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)

        except Exception as e:
            reply_local = f"❌ Sorry, something went wrong.\n\n{str(e)}"
            audio_fp = None

    # Show bot reply and optional audio
    st.markdown(f"<div class='chat-container'><div class='chat-message bot'>{reply_local}</div></div>", unsafe_allow_html=True)
    if audio_fp:
        st.audio(audio_fp, format="audio/mp3")

    # Save to session
    st.session_state.chat_history.append({
        "user": prompt,
        "bot": reply_local,
        "audio": audio_fp.getvalue() if audio_fp else None
    })
