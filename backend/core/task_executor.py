"""
Task Executor + Voice Loop for Friday AI

Dispatches to intent handlers or LLM via /chat API.
Also provides run_voice_loop() — a full spoken conversation CLI.
"""

import os
import requests
from typing import Optional

from backend.core.nlp_engine import classify_intent
from backend.core.tts_engine import speak
from backend.core.speech_listener import listen_command
from backend.intents.open_app import open_application
from backend.intents.search_web import search_and_summarize

CHAT_URL = os.getenv("FRIDAY_BACKEND_URL", "http://localhost:8000") + "/chat"


# ---------------------------------------------------------------------------
# Execute a classified intent (non-LLM actions)
# ---------------------------------------------------------------------------

def execute_task(intent: str, entity: str, raw_command: str = "") -> Optional[str]:
    """
    Handle action intents directly (no LLM needed).

    Returns:
        str  — friendly response text  (for action intents)
        None — if intent should be routed to the LLM
    """
    if intent == "open_app":
        return open_application(entity)

    elif intent == "search_web":
        results = search_and_summarize(entity)
        return f"Here is what I found:\n{results}"

    elif intent == "system_control":
        if "shutdown" in raw_command:
            speak("Shutting down your system now. Goodbye.")
            os.system("shutdown /s /t 3")
            return "Initiating system shutdown."
        elif "restart" in raw_command:
            speak("Restarting your system. See you soon.")
            os.system("shutdown /r /t 3")
            return "Initiating system restart."
        return "System control command not recognised."

    elif intent == "greet":
        return "Hello! I am Friday, your AI assistant. How can I help you today?"

    # intent == "chat" or unknown → route to LLM
    return None


# ---------------------------------------------------------------------------
# Send a text message to the LLM /chat endpoint and collect full response
# ---------------------------------------------------------------------------

def ask_friday(message: str, history: list = None) -> str:
    """POST to /chat and return the full streamed response as a string."""
    payload = {"message": message, "history": history or []}
    try:
        response = requests.post(CHAT_URL, json=payload, stream=True, timeout=60)
        response.raise_for_status()
        full_response = ""
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                full_response += chunk.decode("utf-8", errors="replace")
        return full_response.strip() or "I'm thinking… could you repeat that?"
    except requests.exceptions.ConnectionError:
        return "I cannot reach my brain right now. Please make sure the backend is running."
    except Exception as e:
        return f"Something went wrong: {e}"


# ---------------------------------------------------------------------------
# Full voice conversation loop (CLI)
# ---------------------------------------------------------------------------

STOP_PHRASES = {"goodbye", "bye", "stop", "exit", "quit", "shut up"}


def run_voice_loop():
    """
    Continuous voice conversation:
      listen → transcribe → intent check → LLM / action → TTS speak
    Say 'goodbye' / 'stop' / 'exit' to end.
    """
    speak("Hello! I am Friday, your personal AI assistant. I am listening.")
    history = []

    print("\n🔊 Voice loop started. Say 'goodbye' to stop.\n")

    while True:
        # 1. Listen
        command = listen_command()
        if command is None:
            speak("I didn't catch that. Could you say it again?")
            continue

        print(f"📝 You said: \"{command}\"")

        # 2. Stop condition
        if any(phrase in command for phrase in STOP_PHRASES):
            speak("Goodbye! Have a wonderful day.")
            print("👋 Voice loop ended.")
            break

        # 3. Classify intent
        intent, entity = classify_intent(command)
        print(f"🧠 Intent: {intent}  |  Entity: {entity}")

        # 4. Handle action intent directly
        action_response = execute_task(intent, entity, command)

        if action_response:
            speak(action_response)
            history.append({"role": "user", "content": command})
            history.append({"role": "assistant", "content": action_response})
        else:
            # 5. Route to LLM
            speak("Let me think about that…")
            llm_response = ask_friday(command, history)
            speak(llm_response)
            history.append({"role": "user", "content": command})
            history.append({"role": "assistant", "content": llm_response})

        # Keep history manageable
        if len(history) > 20:
            history = history[-20:]


# ---------------------------------------------------------------------------
# Standalone test — run:  python -m backend.core.task_executor
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Friday Voice Loop Test ===")
    run_voice_loop()
