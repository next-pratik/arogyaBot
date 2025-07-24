import streamlit as st
import asyncio

# ✅ Patch for missing event loop on Windows
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from src.main import run_query

st.set_page_config(page_title="🩺 ArogyaBot", layout="centered")
st.title("🩺 ArogyaBot – Ask about your health!")

query = st.text_input("Ask a health question:")
if query:
    response = run_query(query)
    st.write(response)
