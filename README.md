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

### Quick Setup

1. **Set up Ollama:** Run `./scripts/setup_ollama.sh` to initialize your local AI instance.
2. **Download Models:** Run `python scripts/download_models.py` to cache embeddings and voice models.
3. **Install Dependencies:** `pip install -r requirements.txt`

### Running Friday

#### 🖥️ CLI Mode (Recommended for Direct Interaction)

**Interactive Mode** - Talk to Friday in your terminal:
```bash
python cli.py
```

**Single Command** - Ask Friday something and get a response:
```bash
python cli.py "search python tutorials"
```

**Voice Mode** - Speak commands (requires microphone):
```bash
python cli.py --voice
```

Or use the Windows launcher:
```powershell
.\friday.ps1                          # Interactive
.\friday.ps1 "search python"         # Single command
.\friday.ps1 -Voice                  # Voice mode
```

#### 🌐 Web UI Mode (Full Stack)

Launch both backend API and Streamlit frontend:
```bash
./start.sh                            # Linux/Mac
.\start.ps1                           # Windows
```

## � Example Commands

Here's what you can ask Friday:

**Search & Information:**
- "Search for Python machine learning"
- "What is artificial intelligence?"
- "Google the latest news"

**Application Control:**
- "Open notepad"
- "Launch Chrome"
- "Start visual studio code"

**System Control:**
- "Shutdown my computer"
- "Restart the system"
- "Volume up"

**General Chat:**
- "Tell me a joke"
- "How are you today?"
- "What's your favorite programming language?"

**Plan for Future:**
- "Check my email"
- "Create a calendar event"
- "Set up a reminder"

## 🛣️ Roadmap & Progress

Currently, the project is moving through its foundational phases:
- [x] Base project architecture, decoupled endpoints, and UI schemas.
- [x] **CLI Mode:** Interactive command-line interface for direct assistant interaction.
- [ ] **Phase 1:** Core loop execution — text chat integrating Streamlit UI to Ollama backbone.
- [ ] **Phase 2:** Advanced Intent execution & Voice integrations (End-to-end processing).
- [ ] **Phase 3:** RAG enhancements via UI and emotional state system integration.