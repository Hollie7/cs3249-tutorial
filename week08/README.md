# CS3249 Tutorial – LangGraph Exercise System

This repository contains a small backend–frontend system designed for the CS3249 tutorial on **Conversational UI and Agentic Reasoning**.  
It demonstrates how multiple reasoning chains — No-RAG, Vector RAG, and Graph RAG — can be orchestrated through **LangGraph** to form an intelligent router agent.

---

## 1. Requirements and Setup

### Environment
- Python 3.10 or higher
- Internet connection for OpenAI API

### Installation

1. **Clone the repository** and create a new environment:
   ```bash
   git clone <repo-url>
   cd cs3249-langgraph-tutorial
   python -m venv venv
   source venv/bin/activate      # or .\venv\Scripts\activate on Windows
   ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a .env file in the project root:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## 2. How to Run
### Backend

Run the backend notebook or script:
```
jupyter notebook backend/rag_backend_exercise.ipynb
```

### Frontend

Launch the Gradio interface:
```
jupyter notebook frontend/gradio_app.ipynb
```

Gradio will open in a browser window with several tabs representing different reasoning modes.


## 3. System Components

| Component            | Description                                                                    | Expected Behavior                                         |
| -------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------- |
| **No-RAG**           | Direct LLM response without retrieval.                                         | Produces general conversational answers.                  |
| **Vector RAG**       | Uses document embeddings and semantic retrieval from `vector_sample_data.txt`. | Answers questions that depend on text content.            |
| **Graph RAG**        | Uses a network-based knowledge graph from `graph_sample_data.json`.            | Answers questions about relationships (e.g., co-authors). |
| **LangGraph Router** | Directs the query to the most appropriate reasoning mode.                      | Detects query type and calls the corresponding chain.     |


## 4. Exercise Tasks
You will implement three improvements in the backend to explore how agent systems manage reasoning and reliability.

| Task                    | Description                                                                  | Example Input                                   | Expected Outcome                                                                |
| ----------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------- |
| **1. Fallback Logic**   | Make LangGraph automatically switch modes if one path fails.                 | “Who are Elon Musk’s coauthors?”                | Graph RAG fails (no data) → fallback to No-RAG for a general answer.            |
| **2. Caching Layer**    | Cache repeated queries to avoid redundant API calls.                         | Ask “Who are Yi-Chieh Lee’s coauthors?” twice.  | The second call returns instantly with a cache hit.                             |
| **3. LLM-based Router** | Replace keyword routing with an LLM that selects the best mode semantically. | “Show me Yi-Chieh Lee’s collaboration network.” | The router interprets it as a Graph RAG query even without the word “coauthor.” |


## 5. API Endpoints Summary
| Endpoint                 | Method | Description                                      |
| ------------------------ | ------ | ------------------------------------------------ |
| `/chat/no_rag`           | POST   | Simple LLM call.                                 |
| `/chat/rag`              | POST   | Vector RAG retrieval-augmented generation.       |
| `/chat/graph_rag`        | POST   | Graph RAG reasoning over a networkx graph.       |
| `/chat/langgraph`        | POST   | LangGraph router combining all chains.           |
| `/tools`                 | GET    | Returns available example tools.                 |
| `/call/get_current_time` | POST   | Example external function returning server time. |


## 6. Notes

- The sample data are small and purely demonstrational.

- API latency depends on the OpenAI model used (gpt-4o-mini by default).

- For real applications, persistent vector stores and more sophisticated routing logic should be implemented.