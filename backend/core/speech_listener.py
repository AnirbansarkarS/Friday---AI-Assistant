"""
Speech-to-Text for Friday AI
Primary: Google Speech Recognition (online)
Fallback: OpenAI Whisper tiny (offline)
"""

import speech_recognition as sr
import tempfile
import os

# ---------------------------------------------------------------------------
# Lazy-load Whisper only when needed (saves startup time if online is fine)
# ---------------------------------------------------------------------------
_whisper_model = None

def _get_whisper():
    global _whisper_model
    if _whisper_model is None:
        try:
            import whisper
            print("🔄 Loading Whisper (tiny) model for offline fallback...")
            _whisper_model = whisper.load_model("tiny")
            print("✅ Whisper loaded.")
        except ImportError:
            print("⚠️  openai-whisper not installed. Offline STT unavailable.")
            _whisper_model = False   # sentinel: don't retry
    return _whisper_model if _whisper_model else None


def _transcribe_with_whisper(audio: sr.AudioData) -> str | None:
    """Save audio to a temp WAV and run Whisper on it."""
    model = _get_whisper()
    if model is None:
        return None
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio.get_wav_data())
            tmp_path = tmp.name
        result = model.transcribe(tmp_path, language="en")
        return result["text"].strip() or None
    except Exception as e:
        print(f"⚠️  Whisper error: {e}")
        return None
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


def listen_command(
    timeout: int = 8,
    phrase_time_limit: int = 10,
    calibrate_duration: float = 1.0,
) -> str | None:
    """
    Listen from the default microphone and return transcribed text.

    Returns:
        str  — transcribed command, lowercase
        None — if nothing was understood
    """
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("🎙️  Calibrating for ambient noise…")
        recognizer.adjust_for_ambient_noise(source, duration=calibrate_duration)
        print("🎤  Listening… (speak now)")
        try:
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )
        except sr.WaitTimeoutError:
            print("⏱️  No speech detected within timeout.")
            return None

    # --- Primary: Google STT ---
    try:
        text = recognizer.recognize_google(audio)
        print(f"✅ [Google STT] Heard: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("❓ Google STT: could not understand audio.")
    except sr.RequestError as e:
        print(f"🌐 Google STT unavailable ({e}). Trying Whisper offline…")

    # --- Fallback: Whisper ---
    text = _transcribe_with_whisper(audio)
    if text:
        print(f"✅ [Whisper] Heard: {text}")
        return text.lower()

    print("❌ Could not transcribe speech.")
    return None


# ---------------------------------------------------------------------------
# Standalone test — run:  python -m backend.core.speech_listener
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Friday STT Validation ===")
    result = listen_command()
    if result:
        print(f"\n📝 Transcript → \"{result}\"")
    else:
        print("\n❌ No transcript obtained. Check microphone connection and try again.")
