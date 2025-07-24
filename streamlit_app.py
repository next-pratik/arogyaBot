import streamlit as st
import asyncio

# ✅ Windows event loop fix
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from src.main import run_query  # Your medical query function

# ✅ Page setup
st.set_page_config(page_title="ArogyaBot – Medical Assistant", layout="wide")

# ✅ Custom styling (clean, centered, dark UI)
st.markdown("""
    <style>
        /* Global dark mode */
        body, .stApp {
            background-color: #000000;
            color: #FFFFFF;
        }

        /* Remove top padding */
        .block-container {
            padding-top: 1.5rem;
        }

        /* Center container */
        .main {
            display: flex;
            justify-content: center;
        }

        .chat-container {
            max-width: 700px;
            width: 100%;
        }

        /* Chat bubbles */
        .chat-bubble {
            padding: 1rem;
            border-radius: 1rem;
            margin-bottom: 1rem;
            font-size: 1.05rem;
            line-height: 1.6;
            color: #ffffff;
            background-color: #1a1a1a;
            word-wrap: break-word;
        }

        .user-msg {
            align-self: flex-end;
            margin-left: auto;
            background-color: #333333;
        }

        .bot-msg {
            align-self: flex-start;
            margin-right: auto;
            background-color: #1a1a1a;
        }

        /* Input box clean style */
        input[type='text'] {
            background-color: #111 !important;
            color: white !important;
            border: none !important;
            border-radius: 0.5rem !important;
            padding: 1rem !important;
        }

        button[kind="primary"] {
            background-color: #222 !important;
            color: white !important;
            border: none !important;
            border-radius: 0.5rem !important;
        }

        /* Hide emojis from chat_message */
        .stChatMessageAvatar {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Title (centered, clean)
st.markdown("<h1 style='text-align: center;'>ArogyaBot – Your Trusted Health Assistant</h1>", unsafe_allow_html=True)

# ✅ Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ Sidebar
with st.sidebar:
    st.markdown("History")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ✅ Chat container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# ✅ Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-bubble user-msg'>{chat['user']}</div>", unsafe_allow_html=True)
    with st.chat_message("assistant"):
        st.markdown(f"<div class='chat-bubble bot-msg'>{chat['bot']}</div>", unsafe_allow_html=True)

# ✅ User input
if prompt := st.chat_input("Ask a medical question..."):
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-bubble user-msg'>{prompt}</div>", unsafe_allow_html=True)

    with st.spinner("Processing..."):
        reply = run_query(prompt)

    with st.chat_message("assistant"):
        st.markdown(f"<div class='chat-bubble bot-msg'>{reply}</div>", unsafe_allow_html=True)

    st.session_state.chat_history.append({"user": prompt, "bot": reply})

st.markdown("</div>", unsafe_allow_html=True)
