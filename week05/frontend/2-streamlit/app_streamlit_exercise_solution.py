# CS3249 — Streamlit Frontend (Sessions + Visualization)
# -----------------------------------------------------
# Features:
# 1) Multi-session management (create/switch/clear sessions)
# 2) Chat interface with temperature & max_tokens
# 3) Simple conversation analytics (message counts, length plot)
#
# Run:
#   streamlit run app_streamlit_sessions_viz.py --server.port 8502

import os
import uuid
import requests
import streamlit as st
import matplotlib.pyplot as plt
import sys, os 
sys.path.append(os.path.abspath("..")) # add parent folder (week05/frontend) 
from config import BACKEND_URL


st.set_page_config(page_title="CS3249 — Streamlit Sessions & Viz", page_icon="💬", layout="wide")
st.title("💬 CS3249 — Streamlit (Sessions + Visualization)")

# ----- Sidebar -----
with st.sidebar:
    st.markdown("### Backend Settings")
    BACKEND_URL = st.text_input("Backend URL", value=BACKEND_URL)

    st.markdown("### Generation Params")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.slider("Max Tokens", 10, 500, 200, 10)

    st.markdown("### Sessions")
    if "all_histories" not in st.session_state:
        st.session_state.all_histories = {}
    if "current_session" not in st.session_state:
        new_id = f"sess-{uuid.uuid4().hex[:6]}"
        st.session_state.current_session = new_id
        st.session_state.all_histories[new_id] = []

    # session selector
    session_ids = sorted(st.session_state.all_histories.keys())
    selected = st.selectbox("Select session", options=session_ids, index=session_ids.index(st.session_state.current_session))
    if selected != st.session_state.current_session:
        st.session_state.current_session = selected

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ New session"):
            new_id = f"sess-{uuid.uuid4().hex[:6]}"
            st.session_state.all_histories[new_id] = []
            st.session_state.current_session = new_id
    with col2:
        if st.button("🗑️ Clear current session"):
            st.session_state.all_histories[st.session_state.current_session] = []

# ----- Helpers -----
def get_history():
    return st.session_state.all_histories[st.session_state.current_session]

def append_turn(role, content):
    st.session_state.all_histories[st.session_state.current_session].append({"role": role, "content": content})

def send_to_backend(msg: str) -> str:
    payload = {
        "message": msg,
        "temperature": float(temperature),
        "max_tokens": int(max_tokens),
        "session_id": st.session_state.current_session,  # ok if backend ignores
    }
    try:
        resp = requests.post(BACKEND_URL, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json().get("response", "[No response]")
    except Exception as e:
        return f"[Frontend error: {e}]"

# ----- Layout -----
left, right = st.columns([2, 1])

# Chat area
with left:
    st.subheader(f"Session: `{st.session_state.current_session}`")

    for turn in get_history():
        with st.chat_message(turn["role"]):
            st.write(turn["content"])

    user_input = st.chat_input("Type your message")
    if user_input:
        append_turn("user", user_input)
        with st.chat_message("user"):
            st.write(user_input)

        reply = send_to_backend(user_input)
        append_turn("assistant", reply)
        with st.chat_message("assistant"):
            st.write(reply)

# Visualization
with right:
    with st.expander("📈 Conversation Analytics", expanded=False):
        hist = get_history()
        if not hist:
            st.info("No messages yet.")
        else:
            user_msgs = [t["content"] for t in hist if t["role"] == "user"]
            bot_msgs  = [t["content"] for t in hist if t["role"] == "assistant"]
            lengths   = [len(t["content"]) for t in hist]

            st.markdown(f"- Total turns: **{len(hist)}**")
            st.markdown(f"- User turns: **{len(user_msgs)}**, Assistant turns: **{len(bot_msgs)}**")

            # line chart of length per turn
            fig, ax = plt.subplots(figsize=(4, 2.5))
            ax.plot(range(1, len(hist) + 1), lengths, marker="o")
            ax.set_xlabel("Turn")
            ax.set_ylabel("Length (chars)")
            ax.set_title("Message Length by Turn")
            st.pyplot(fig, clear_figure=True)

            # bar chart of role counts
            st.bar_chart({"User": len(user_msgs), "Assistant": len(bot_msgs)})
