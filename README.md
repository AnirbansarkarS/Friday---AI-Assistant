# Friday - Personal AI Assistant

Friday is a personal, locally-hosted AI assistant. It integrates Retrieval-Augmented Generation (RAG), Natural Language Processing (local LLM inference via Ollama), Voice capabilities (Speech-to-Text and Text-to-Speech), and system-level task execution.

## 🌟 Key Features

* **100% Local & Private**: No data leaves your machine. Powered by local LLMs via Ollama.
* **Retrieval-Augmented Generation (RAG)**: Chat with your own PDFs and documents using a local vector store (ChromaDB).
* **Voice Interaction**: Built-in Speech-to-Text (STT) and Text-to-Speech (TTS) for natural conversations.
* **System Control & Automation**: Launch applications, control system settings, and perform web searches directly through conversational intents.
* **Personality & Emotional State**: (Planned) Friday will retain memory and compute an emotional state based on interactions to generate realistic and dynamic responses.

## 🏗️ Project Architecture

The project is decoupled into three main segments:

1. **Frontend UI** (Streamlit): Easy-to-use chat interface, document uploader for RAG, and settings adjustment.
2. **Backend API** (FastAPI): Bridging the UI and the Core AI engine. Organized via distinct routes for chat, document ingestion, and health monitoring.
3. **Core AI Engine & Intents**: 
   * Handlers for LLM Inference, STT/TTS, and Memory contexts.
   * Action Intents mapping to OS-level system executions (`open_app.py`, `system_control.py`, `search_web.py`).

## 📂 Repository Structure

```text
Friday---AI-Assistant/
├── backend/            # Core AI engines, REST API mapping, and intent handling
│   ├── core/           # Local Inference, STT/TTS, RAG, Task Executor
│   ├── intents/        # Web Search, System Control, App Opening plugins
│   ├── routes/         # Modular FastApi endpoints
│   └── utils/          # ChromaDB, doc loaders (PDF, Text Splitters)
├── frontend/           # Presentation layer built with Streamlit
│   └── pages/          # Chatbot UI, Doc Upload UI, Settings
├── data/               # Local persistent storage for memory and vector DB
└── scripts/            # Helper scripts to set up Ollama and download models
```

## 🚀 Getting Started

*Note: The project is actively under development.*

1. **Set up Ollama:** Run `./scripts/setup_ollama.sh` to initialize your local AI instance.
2. **Download Models:** Run `python scripts/download_models.py` to cache embeddings and voice models.
3. **Install Dependencies:** `pip install -r requirements.txt`
4. **Boot up:** Use the provided `./start.sh` script to launch both the backend API and frontend app simultaneously.

## 🛣️ Roadmap & Progress

Currently, the project is moving through its foundational phases:
- [x] Base project architecture, decoupled endpoints, and UI schemas.
- [ ] **Phase 1:** Core loop execution — text chat integrating Streamlit UI to Ollama backbone.
- [ ] **Phase 2:** Advanced Intent execution & Voice integrations (End-to-end processing).
- [ ] **Phase 3:** RAG enhancements via UI and emotional state system integration.