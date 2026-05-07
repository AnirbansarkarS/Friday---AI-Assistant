# Project Progress: Friday - AI Assistant

## Overview
Friday is a personal, locally-hosted AI assistant. It integrates Retrieval-Augmented Generation (RAG), Natural Language Processing (local LLM inference via Ollama), Voice capabilities (Speech-to-Text and Text-to-Speech), and system-level task execution.

## Current Progress & Working Status

**Overall Progress Estimation: ~65% - 75% Complete**

### What is Currently Working 💪
*   **Base Project Architecture:** The modular structure (decoupling frontend UI, backend APIs, core AI logic, and data storage) is fully established and mapped out.
*   **Frontend UI Definition:** The Streamlit application structure (`app.py`, `chatbot.py`, `Upload_Doc_RAG.py`) is laid out for user interaction.
*   **Backend API Services:** API routes (`chat.py`, `rag.py`, `health.py`) and clients (`api_client.py`) are logically defined to bridge the user interface with the local AI models.
*   **Core AI Pipelines (Code Structure):** The logic files for Local Inference (`inference.py`), STT/TTS (`speech_listener.py`, `tts_engine.py`), and intent actions (`open_app.py`, `search_web.py`) are created and organized.

### What Needs Testing/Validation 🚧
*   **End-to-End Execution:** Running a full conversation cycle from the Streamlit UI -> Backend API -> Ollama Model -> UI response.
*   **Voice & Hardware Integration:** Validating that `speech_listener.py` successfully captures valid microphone input and `tts_engine.py` outputs clear audio.
*   **Database Connections:** Confirming ChromaDB successfully persists and retrieves embeddings for the RAG pipeline.

## Current Architecture & Completed Components

### 1. Backend (`/backend`)
The backend is structured to separate concerns between the core AI engines, the REST APIs, and specific intent handlers.

*   **Core Engine (`/backend/core`)**:
    *   **Local Inference**: `nlp_engine.py`, `inference.py`, and `model.py` handle communicating with local LLMs.
    *   **Memory & RAG**: `rag.py` and `embedding.py` map user queries to vectorized context.
    *   **Voice Integration**: `speech_listener.py` (STT) and `tts_engine.py` (TTS) enable vocal interaction.
    *   **Execution**: `task_executor.py` processes commands effectively.
*   **Action Intents (`/backend/intents`)**:
    *   System execution handlers: `open_app.py` for launching applications, `system_control.py` for OS modifications, and `search_web.py` for web querying.
*   **API Routes (`/backend/routes`)**:
    *   Modular external endpoints: `chat.py` (messaging), `rag.py` (document knowledge querying), and `health.py` (monitoring).
*   **Utilities (`/backend/utils`)**:
    *   `chroma_db.py`: Vector store interfacing.
    *   `pdf_loader.py` & `text_splitter.py`: Pipelines for parsing and chunking documents.

### 2. Frontend (`/frontend`)
The presentation layer is built to manage complex interactions simply, utilizing Streamlit (based on standard file naming conventions).

*   `app.py`: Main entry mechanism.
*   **Pages (`/frontend/pages`)**: 
    *   `chatbot.py`: Conversational UI interface interacting with the backend capabilities.
    *   `Upload_Doc_RAG.py`: Drag-and-drop document upload interface to append data to ChromaDB.
    *   `settings.py`: Model and system configuration modifications.
*   `helpers/api_client.py`: Dedicated client to connect the frontend UI to backend services robustly.

### 3. Data & Infrastructure
*   `data/docs/` & `data/vectorstore/`: Local persistent storage configurations.
*   **Scripts (`/scripts`)**:
    *   `setup_ollama.sh`: Automated configuration for Ollama instances.
    *   `download_models.py`: Helper script to cache embeddings, STT, and TTS models for offline availability.

## Implementation Roadmap

### Phase 1: Core loop — text chat works
*Goal: Get Ollama talking to the Streamlit UI end-to-end. No voice, no RAG yet.*

*   [ ] **Start Ollama + Pull Model:**
    *   Run `ollama serve`, pull `llama3` or `mistral`.
    *   Confirm it responds via curl in the terminal.
*   [ ] **Wire `inference.py` (Local LLM Integration):**
    *   File: `/backend/core/inference.py`
    *   Call Ollama `/api/generate`. Return streamed tokens. 
    *   Add system prompt for the emotional companion persona.
*   [ ] **Build `/chat` Route:**
    *   File: `/backend/routes/chat.py`
    *   FastAPI `POST /chat`. Accepts message + history. Returns streamed LLM response.
*   [ ] **Streamlit Chat UI:**
    *   File: `/frontend/pages/chatbot.py`
    *   Use `st.chat_input` and `st.chat_message`. 
    *   Call `api_client` -> `/chat`. Stream tokens into the UI.

## Next Steps / Backlog
*   [ ] **End-to-End Testing**: Confirm the complete pipeline (Voice -> Intent -> Search -> Local LLM -> TTS).
*   [ ] **Expand Intents**: Add more plugins (`/backend/intents/`) like Email fetching, Calendar integration, or IoT smart home controls.
*   [ ] **Optimization**: Test latency times for local Ollama instances and experiment with lighter quantized text and embedding models.
*   [ ] **Deployment**: Create a `docker-compose.yml` for unified initialization of both the backend and frontend components.

## 🧬 Planned Feature: Emotional State System
**Core Idea**: Give Friday an internal state to create the illusion of life. The same user input will generate different responses based on Friday's current "mood."

**Proposed State Structure:**
```json
{
  "mood": "calm",
  "energy": 0.7,
  "bond_with_user": 0.4,
  "last_interaction_sentiment": "positive"
}
```
*Note: This structure will be expanded as needed to include more dynamic traits and personality dimensions.*