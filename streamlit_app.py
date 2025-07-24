import asyncio
import sys
import base64
import streamlit as st
import streamlit.components.v1 as components
from io import BytesIO
from gtts import gTTS
from src.logic import process_user_prompt

# Fix event loop issue on Windows
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop(asyncio.new_event_loop())
    except RuntimeError:
        pass

# Streamlit page setup
st.set_page_config(page_title="ArogyaBot – Medical Assistant", layout="centered")

# Custom styling
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
            position: relative;
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

st.markdown("<h1 style='text-align:center;'>ArogyaBot – Your Trusted Health Assistant</h1>", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar: Clear chat history
with st.sidebar:
   
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Display chat messages
for idx, chat in enumerate(st.session_state.chat_history):
    st.markdown(f"<div class='chat-container'><div class='chat-message user'>{chat['user']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-container'><div class='chat-message bot'>{chat['bot']}</div></div>", unsafe_allow_html=True)

    if chat.get("audio"):
        b64_audio = base64.b64encode(chat["audio"]).decode()
        components.html(f"""
            <div style="text-align: left; margin-top: -10px; margin-bottom: 20px;">
                <span onclick="document.getElementById('audio{idx}').play()"
                      style="cursor: pointer; font-size: 24px;"
                      title="Play audio">
                    🎙️
                </span>
                <audio id="audio{idx}" src="data:audio/mp3;base64,{b64_audio}"></audio>
            </div>
        """, height=40)

# Handle user prompt
if prompt := st.chat_input("Ask a medical question in any language..."):
    st.markdown(f"<div class='chat-container'><div class='chat-message user'>{prompt}</div></div>", unsafe_allow_html=True)

    with st.spinner("Processing..."):
        reply_text, audio_fp = process_user_prompt(prompt)

    st.markdown(f"<div class='chat-container'><div class='chat-message bot'>{reply_text}</div></div>", unsafe_allow_html=True)

    audio_bytes = audio_fp.getvalue() if audio_fp else None
    if audio_bytes:
        b64_audio = base64.b64encode(audio_bytes).decode()
        idx = len(st.session_state.chat_history)
        components.html(f"""
            <div style="text-align: left; margin-top: -10px; margin-bottom: 20px;">
                <span onclick="document.getElementById('audio{idx}').play()"
                      style="cursor: pointer; font-size: 24px;"
                      title="Play audio">
                    🎙️
                </span>
                <audio id="audio{idx}" src="data:audio/mp3;base64,{b64_audio}"></audio>
            </div>
        """, height=40)

    st.session_state.chat_history.append({
        "user": prompt,
        "bot": reply_text,
        "audio": audio_bytes
    })
