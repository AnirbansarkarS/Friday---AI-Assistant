from fastapi import FastAPI
from pydantic import BaseModel

from backend.core.speech_listener import listen_command
from backend.core.nlp_engine import classify_intent
from backend.core.task_executor import execute_task, ask_friday
from backend.core.tts_engine import speak
from backend.routes.chat import router as chat_router
from backend.routes.rag import router as rag_router

app = FastAPI(title="Friday AI Backend", version="1.0.0")

# Register routers
app.include_router(chat_router)
app.include_router(rag_router)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/")
def home():
    return {"message": "Friday AI Backend Online ✅"}


# ---------------------------------------------------------------------------
# /listen — server-side mic → STT → intent → (action | LLM)
# ---------------------------------------------------------------------------

@app.get("/listen")
def listen_endpoint():
    """
    Trigger the server microphone, transcribe speech, route through intent
    classifier, and return the command + response.
    """
    command = listen_command()
    if not command:
        return {"error": "Could not understand the audio. Please try again."}

    intent, entity = classify_intent(command)
    action_response = execute_task(intent, entity, raw_command=command)

    if action_response:
        response = action_response
    else:
        # Route to LLM
        response = ask_friday(command)

    return {
        "command": command,
        "intent": intent,
        "entity": entity,
        "response": response,
    }


# ---------------------------------------------------------------------------
# /speak — TTS endpoint (used by Streamlit voice mode)
# ---------------------------------------------------------------------------

class SpeakRequest(BaseModel):
    text: str


@app.post("/speak")
def speak_endpoint(req: SpeakRequest):
    """Speak text aloud on the server machine."""
    speak(req.text)
    return {"spoken": req.text}
