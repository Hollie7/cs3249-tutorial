import os
import uuid
import requests
import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="CS3249 CUI (Streamlit)", page_icon="💬", layout="centered")
st.title("💬 CS3249 — Minimal CUI (Streamlit)")

# ---------- Sidebar controls ----------
with st.sidebar:
    st.markdown("### Backend Settings")
    backend_default = os.getenv("CS3249_BACKEND_URL", "http://localhost:8001/chat")
    BACKEND_URL = st.text_input("Backend URL", value=backend_default, help="POST endpoint for /chat")

    st.markdown("### Generation Params")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.slider("Max Tokens", 10, 500, 200, 10)

    st.markdown("### Session")
    # Create or edit a session_id that we’ll send to backend (if supported)
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"sess-{uuid.uuid4().hex[:8]}"
    st.session_state.session_id = st.text_input("Session ID", value=st.session_state.session_id)

    clear = st.button("Clear Conversation")

# ---------- Initialize history ----------
if "history" not in st.session_state or clear:
    st.session_state.history = []  # list of {"role": "user"/"assistant", "content": "..."}

# ---------- Render history ----------
for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.write(turn["content"])

# ---------- Message sender ----------
def send_to_backend(user_text: str) -> str:
    """POST to backend and return assistant text (or error)."""
    payload = {
        "message": user_text,
        # Forward optional params; harmless if backend ignores them
        "temperature": float(temperature),
        "max_tokens": int(max_tokens),
        "session_id": st.session_state.session_id,  # ok if backend ignores
    }
    try:
        resp = requests.post(BACKEND_URL, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        # Expect {"response": "..."}; fall back to raw text
        return data.get("response") or resp.text
    except Exception as e:
        return f"[Frontend error: {e}]"

# ---------- Chat input ----------
user_input = st.chat_input("Type your message and press Enter")
if user_input:
    # show user message
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # get assistant reply
    reply = send_to_backend(user_input)
    st.session_state.history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)