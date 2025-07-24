import asyncio
import sys

if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop(asyncio.new_event_loop())
    except RuntimeError:
        pass

import streamlit as st
from src.logic import process_user_prompt

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

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.markdown("### 🕓 Chat History")
    if st.button("🧹 Clear"):
        st.session_state.chat_history = []
        st.rerun()

# Display past chats
for chat in st.session_state.chat_history:
    st.markdown(f"<div class='chat-container'><div class='chat-message user'>{chat['user']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-container'><div class='chat-message bot'>{chat['bot']}</div></div>", unsafe_allow_html=True)
    if chat.get("audio"):
        st.audio(chat["audio"], format="audio/mp3")

# Input box
if prompt := st.chat_input("Ask a medical question in any language..."):
    st.markdown(f"<div class='chat-container'><div class='chat-message user'>{prompt}</div></div>", unsafe_allow_html=True)

    with st.spinner("Processing..."):
        reply_local, audio_fp = process_user_prompt(prompt)

    st.markdown(f"<div class='chat-container'><div class='chat-message bot'>{reply_local}</div></div>", unsafe_allow_html=True)
    if audio_fp:
        st.audio(audio_fp, format="audio/mp3")

    st.session_state.chat_history.append({
        "user": prompt,
        "bot": reply_local,
        "audio": audio_fp.getvalue() if audio_fp else None
    })
