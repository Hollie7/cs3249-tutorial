# CS3249 Tutorial 05: Conversational UI Frontends

This tutorial shows how to build **Conversational UIs (CUI)** using different tools.  
We will connect simple backends (Ollama or GPT API) with three frontends: **Gradio**, **Streamlit**, and **React**.

---

### 1. Backend (choose one)

- **GPT API backend**
  - Requiremnents:
    - An OpenAI account
    - An API key from the API Keys page
    - Save the key into a `.env` file at the project root:
        ```
        OPENAI_API_KEY=sk-xxxxxxx
        ```
  - Open `backend_api.ipynb` in Jupyter Notebook.
  - Make sure you have an `OPENAI_API_KEY` saved in a `.env` file.

- **Ollama backend**
  - Requirements:
    - Install Ollama
    - Make sure the Ollama server is running (usually it runs automatically after installation, but you can start it manually):
      ```
      ollama serve
      ```
    - Pull a model you want to use, e.g.:
      ```
      ollama pull phi3:mini
      ```
  - Open `backend_ollama.ipynb` in Jupyter Notebook.
  - Make sure [Ollama](https://ollama.com) is installed and that you have pulled a model (e.g., `phi3:mini`).

Both backends start a FastAPI server at: http://localhost:8001/chat


---

### 2. Gradio frontend
- Open `frontend/1-gradio/frontend_gradio.ipynb` in Jupyter Notebook.
- This will launch a Gradio app (default at `http://localhost:7860`).


- **Currently implemented:**
    - Minimal chatbot interface with input box and conversation history.
    - Supports multi-turn conversation with the backend.

- **Exercises:**
    - Add export/save function for conversation history.
    - Add file upload and enable simple Q&A with file contents.
    - Add parameter controls (temperature, max_tokens) in a sidebar.


### 3. Streamlit frontend

- **(Recommended)** Run Streamlit apps from the **command line** (not inside Jupyter):
  ```bash
  streamlit run frontend/2-streamlit/app_streamlit_minimal.ipynb
  ```

- You can replace app_streamlit_minimal.ipynb with app_streamlit.ipynb or other files.

- Alternative (not best practice):
For convenience, we also provide a notebook (frontend_streamlit.ipynb) that has cells like:

    ```
    !streamlit run app_streamlit_minimal.py --server.port 8502 --server.headless true
    ```

- This lets you launch Streamlit from inside Jupyter, but it’s not recommended for real projects.
Use it only when experimenting quickly.
- Open in browser at http://localhost:8502.


- **Currently implemented:**

    - Minimal chatbot interface (send messages, get replies).

    - Extended version includes: temperature/max_tokens settings, multiple sessions, conversation visualization.

- **Exercises:** Complete the app_streamlit_exercise.ipynb by implementing:

    - Multi-session management (new session, switch, clear).

    - Backend call with parameters.

    - Conversation analytics (counts, charts).

---
### 4. React frontend

- We only provide `App.tsx`.
- You can create your own React + TypeScript project (e.g., with Vite):

    ```bash
    npm create vite@latest cui-minimal -- --template react-ts
    cd cui-minimal
    npm install
    ```

- Replace `src/App.tsx` with the provided file.

- Run:
    ```bash
    npm run dev
    ```

- Open in browser at http://localhost:5173.


- **Currently implemented:**

    - Minimal chatbox with input and multi-turn conversation.

    - Sends user message to backend and displays assistant replies.

- **Exercises (open-ended):**

    - Improve UI styling (message bubbles, alignment).

    - Explore using React libraries (e.g., Material UI, Tailwind) for richer UI.