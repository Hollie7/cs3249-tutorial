import requests
import streamlit as st

BACKEND_URL = "http://localhost:8001/chat"  # adjust if backend runs elsewhere

st.set_page_config(page_title="CS3249 Minimal CUI", page_icon="💬")
st.title("💬 CS3249 — Minimal CUI (Streamlit)")

# Initialize conversation history
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"role": "...", "content": "..."}

# Render history
for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.write(turn["content"])

# Send message to backend
def send_message(user_text: str) -> str:
    try:
        resp = requests.post(BACKEND_URL, json={"message": user_text}, timeout=60)
        resp.raise_for_status()
        return resp.json().get("response", "[No response]")
    except Exception as e:
        return f"[Error contacting backend: {e}]"

# Chat input
user_input = st.chat_input("Type your message")
if user_input:
    # Show user message
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get assistant reply
    reply = send_message(user_input)
    st.session_state.history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
