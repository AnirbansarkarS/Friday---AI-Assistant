"""
Text-to-Speech engine for Friday AI
Uses pyttsx3 — fully offline, no API key needed.
Selects a calm/female voice automatically (Zira on Windows).
"""

import pyttsx3
from typing import Optional

# ---------------------------------------------------------------------------
# Engine initialisation (module-level singleton)
# ---------------------------------------------------------------------------
_engine: Optional[pyttsx3.Engine] = None


def _init_engine() -> pyttsx3.Engine:
    """Initialise pyttsx3 engine and apply voice / rate settings."""
    engine = pyttsx3.init()

    # ---- Voice selection: prefer female / calm voices ----
    voices = engine.getProperty("voices")
    preferred_keywords = ["zira", "hazel", "susan", "female", "woman"]
    chosen_voice = None

    for keyword in preferred_keywords:
        for voice in voices:
            if keyword in voice.name.lower() or keyword in voice.id.lower():
                chosen_voice = voice
                break
        if chosen_voice:
            break

    if chosen_voice:
        engine.setProperty("voice", chosen_voice.id)
        print(f"🎙️  TTS voice selected: {chosen_voice.name}")
    else:
        # Fall back to default (first available)
        if voices:
            engine.setProperty("voice", voices[0].id)
            print(f"🎙️  TTS voice (default): {voices[0].name}")

    # ---- Speech parameters ----
    engine.setProperty("rate", 160)      # words per minute — calm pace
    engine.setProperty("volume", 1.0)    # max volume

    return engine


def _get_engine() -> pyttsx3.Engine:
    global _engine
    if _engine is None:
        _engine = _init_engine()
    return _engine


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def speak(text: str) -> None:
    """Speak the given text synchronously."""
    if not text or not text.strip():
        return
    print(f"🤖 Friday: {text}")
    engine = _get_engine()
    engine.say(text)
    engine.runAndWait()


def list_available_voices() -> list[dict]:
    """Return info about all TTS voices on this system (for debugging)."""
    engine = _get_engine()
    return [
        {"id": v.id, "name": v.name, "languages": v.languages}
        for v in engine.getProperty("voices")
    ]


# ---------------------------------------------------------------------------
# Standalone test — run:  python -m backend.core.tts_engine
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Friday TTS Validation ===")
    print("\nAvailable voices:")
    for v in list_available_voices():
        print(f"  • {v['name']} ({v['id']})")

    print("\nSpeaking test sentence…")
    speak("Hello, I am Friday, your personal assistant.")
    print("✅ TTS test complete.")
