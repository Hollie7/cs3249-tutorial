import os
import uuid
import streamlit as st
import matplotlib.pyplot as plt   # for analytics (students will use)

# =============== Config ===============
DEFAULT_BACKEND_URL = os.getenv("CS3249_BACKEND_URL", "http://localhost:8001/chat")

st.set_page_config(page_title="CS3249 — Sessions & Viz (Student)", page_icon="💬", layout="wide")
st.title("💬 CS3249 — Streamlit (Sessions + Visualization) — STUDENT VERSION")

# =============== Sidebar ===============
with st.sidebar:
    st.markdown("### Backend Settings")
    backend_url = st.text_input("Backend URL", value=DEFAULT_BACKEND_URL)

    st.markdown("### Generation Params")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.slider("Max Tokens", 10, 500, 200, 10)

    st.markdown("### Sessions")
    # NOTE: We give you a fixed "default" session so the page loads.
    # You will implement *true* multi-session below.
    if "current_session" not in st.session_state:
        st.session_state.current_session = "default"

    # Container that SHOULD hold histories for *all* sessions:
    # Expected shape: { session_id: [ {role: "user"/"assistant", content: "..."} , ... ] }
    if "all_histories" not in st.session_state:
        st.session_state.all_histories = {"default": []}

    # ----- UI controls for sessions -----
    session_ids = sorted(list(st.session_state.all_histories.keys()))
    selected = st.selectbox("Select session", options=session_ids,
                            index=session_ids.index(st.session_state.current_session)
                            if st.session_state.current_session in session_ids else 0)

    col1, col2 = st.columns(2)
    with col1:
        new_session_btn = st.button("➕ New session")
    with col2:
        clear_session_btn = st.button("🗑️ Clear current session")

# =============== Helpers (STUBS to fill) ===============
def create_new_session() -> None:
    """
    TODO (Sessions): Create a new session_id (e.g., 'sess-xxxxxx') and add an empty history list
    to st.session_state.all_histories, then set st.session_state.current_session to the new id.

    Hints:
      - Use uuid.uuid4().hex[:6] to get a short unique suffix.
      - Initialize the new session's history as [].
    """
    st.info("TODO: implement create_new_session()")
    # Example of what you'd do (remove after implementing):
    # new_id = f"sess-{uuid.uuid4().hex[:6]}"
    # st.session_state.all_histories[new_id] = []
    # st.session_state.current_session = new_id


def switch_session(target_session_id: str) -> None:
    """
    TODO (Sessions): Switch current session to `target_session_id`.
    Make sure the id exists in st.session_state.all_histories.
    """
    st.info("TODO: implement switch_session()")
    # Example:
    # if target_session_id in st.session_state.all_histories:
    #     st.session_state.current_session = target_session_id


def clear_current_session() -> None:
    """
    TODO (Sessions): Clear the history of the current session.
    """
    st.info("TODO: implement clear_current_session()")
    # Example:
    # st.session_state.all_histories[st.session_state.current_session] = []


def get_history() -> list[dict]:
    """
    TODO (Sessions): Return the history list for the *current* session.
    Must read from st.session_state.all_histories[st.session_state.current_session].

    For now, we return the default session so the app renders.
    """
    # Replace the line below with your session-aware history:
    return st.session_state.all_histories.get(st.session_state.current_session, [])


def append_turn(role: str, content: str) -> None:
    """
    TODO (Sessions): Append a message to the *current* session's history.
    """
    st.info("TODO: implement append_turn()")
    # Example:
    # st.session_state.all_histories[st.session_state.current_session].append({"role": role, "content": content})


def send_to_backend(msg: str, *, backend_url: str, temperature: float, max_tokens: int, session_id: str) -> str:
    """
    TODO (Chat): POST to your backend with JSON payload:
        {
          "message": msg,
          "temperature": temperature,
          "max_tokens": max_tokens,
          "session_id": session_id
        }
    And return the assistant's text from the JSON response (e.g., data["response"]).

    Requirements:
      - Handle network errors (try/except) and return a readable error string.
      - Respect the provided backend_url argument (do NOT hardcode).
    """
    # Remove this stub line once implemented:
    return "[TODO] Backend call not implemented. (Echo) " + msg


def compute_analytics(history: list[dict]) -> dict:
    """
    TODO (Analytics): From the given history (list of {role, content}),
    compute at least:
      - total_turns: int
      - user_turns: int
      - assistant_turns: int
      - lengths: list[int]  (length of each message's content in characters)

    Return a dict, e.g.:
      {
        "total_turns": ...,
        "user_turns": ...,
        "assistant_turns": ...,
        "lengths": [...],
      }
    """
    st.info("TODO: implement compute_analytics()")
    # Minimal placeholder so the UI doesn't crash:
    return {
        "total_turns": len(history),
        "user_turns": sum(1 for t in history if t.get("role") == "user"),
        "assistant_turns": sum(1 for t in history if t.get("role") == "assistant"),
        "lengths": [len(t.get("content", "")) for t in history],
    }


def render_analytics_charts(analytics: dict) -> None:
    """
    TODO (Analytics): Given the analytics dict, render:
      - Two markdown bullets with counts
      - A simple length-per-turn line plot using matplotlib
      - (Optional) A role-count bar chart using st.bar_chart

    Tips:
      - Use st.pyplot(fig) to show matplotlib figures.
      - Use range(1, N+1) for x-axis turns.
    """
    st.info("TODO: implement render_analytics_charts()")
    # Example (remove after implementing):
    # import matplotlib.pyplot as plt
    # st.markdown(f"- Total turns: **{analytics['total_turns']}**")
    # st.markdown(f"- User: **{analytics['user_turns']}**, Assistant: **{analytics['assistant_turns']}**")
    # fig, ax = plt.subplots(figsize=(4, 2.5))
    # ax.plot(range(1, len(analytics["lengths"])+1), analytics["lengths"], marker="o")
    # ax.set_xlabel("Turn"); ax.set_ylabel("Length (chars)"); ax.set_title("Message Length by Turn")
    # st.pyplot(fig)
    # st.bar_chart({"User": analytics["user_turns"], "Assistant": analytics["assistant_turns"]})


# =============== Wire up session controls ===============
# Switch to selected session in the Selectbox
switch_session(selected)

if new_session_btn:
    create_new_session()

if clear_session_btn:
    clear_current_session()

# =============== Layout: Chat (left) & Analytics (right) ===============
left, right = st.columns([2, 1])

# --------- LEFT: Chat ----------
with left:
    st.subheader(f"Session: `{st.session_state.current_session}`")

    # Render history
    for turn in get_history():
        with st.chat_message(turn.get("role", "user")):
            st.write(turn.get("content", ""))

    # Chat input
    user_input = st.chat_input("Type your message")
    if user_input:
        append_turn("user", user_input)
        with st.chat_message("user"):
            st.write(user_input)

        # Call backend (students implement)
        reply = send_to_backend(
            user_input,
            backend_url=backend_url,
            temperature=float(temperature),
            max_tokens=int(max_tokens),
            session_id=st.session_state.current_session,
        )
        append_turn("assistant", reply)
        with st.chat_message("assistant"):
            st.write(reply)

# --------- RIGHT: Analytics (collapsible) ----------
with right:
    with st.expander("📈 Conversation Analytics", expanded=False):
        hist = get_history()
        if not hist:
            st.info("No messages yet.")
        else:
            analytics = compute_analytics(hist)
            render_analytics_charts(analytics)