"""
Friday AI — Chatbot Page
Supports both text mode and voice mode (mic toggle).
"""

import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("FRIDAY_BACKEND_URL", "http://localhost:8000")


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Friday — AI Assistant",
    page_icon="🤖",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "voice_mode" not in st.session_state:
    st.session_state.voice_mode = False


# ---------------------------------------------------------------------------
# Sidebar — controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Friday Controls")

    # Voice toggle
    voice_label = "🎙️ Voice Mode: ON" if st.session_state.voice_mode else "🔇 Voice Mode: OFF"
    if st.button(voice_label, use_container_width=True):
        st.session_state.voice_mode = not st.session_state.voice_mode
        st.rerun()

    st.divider()

    st.markdown("**Mode**")
    mode_badge = "🟢 Voice" if st.session_state.voice_mode else "⌨️ Text"
    st.info(mode_badge)

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Friday v1.0 — local AI assistant")


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🤖 Friday")
st.caption("Your personal AI companion — always here.")


# ---------------------------------------------------------------------------
# Render existing chat history
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---------------------------------------------------------------------------
# Helper: call /chat endpoint and collect streamed response
# ---------------------------------------------------------------------------
def stream_response(user_message: str) -> str:
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[-10:]
    ]
    payload = {"message": user_message, "history": history}

    try:
        with requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            stream=True,
            timeout=60,
        ) as resp:
            resp.raise_for_status()
            full = ""
            response_placeholder = st.empty()
            for chunk in resp.iter_content(chunk_size=None):
                if chunk:
                    full += chunk.decode("utf-8", errors="replace")
                    response_placeholder.markdown(full + "▌")
            response_placeholder.markdown(full)
            return full
    except requests.exceptions.ConnectionError:
        return "⚠️ Cannot reach Friday's backend. Make sure the server is running."
    except Exception as e:
        return f"⚠️ Error: {e}"


# ---------------------------------------------------------------------------
# Helper: TTS — speak response text via backend or local pyttsx3 fallback
# ---------------------------------------------------------------------------
def tts_speak(text: str):
    """Best-effort TTS: try server-side speak endpoint, fall back silently."""
    try:
        requests.post(f"{BACKEND_URL}/speak", json={"text": text}, timeout=10)
    except Exception:
        pass  # Non-fatal — voice may not be wired on server side yet


# ---------------------------------------------------------------------------
# VOICE MODE — trigger listen via backend /listen endpoint
# ---------------------------------------------------------------------------
if st.session_state.voice_mode:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        listen_btn = st.button("🎤  Click to Listen", use_container_width=True, type="primary")

    status_ph = st.empty()

    if listen_btn:
        status_ph.info("🎙️  **Listening…** Speak now.")

        try:
            listen_resp = requests.get(f"{BACKEND_URL}/listen", timeout=30)
            listen_resp.raise_for_status()
            data = listen_resp.json()
        except requests.exceptions.ConnectionError:
            status_ph.error("⚠️ Backend not reachable.")
            data = {}
        except Exception as e:
            status_ph.error(f"⚠️ Error: {e}")
            data = {}

        if data.get("command"):
            transcript = data["command"]
            status_ph.success(f"🗣️  **You said:** {transcript}")

            # Show user bubble
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.markdown(transcript)

            # Get Friday's response
            status_ph.info("🧠  **Thinking…**")
            with st.chat_message("assistant"):
                response = stream_response(transcript)

            st.session_state.messages.append({"role": "assistant", "content": response})

            # TTS
            status_ph.info("🔊  **Speaking…**")
            tts_speak(response)
            status_ph.empty()

        elif data.get("error"):
            status_ph.warning(f"❓ {data['error']}")
        else:
            status_ph.warning("❓ Couldn't understand. Try again.")

    st.markdown("---")


# ---------------------------------------------------------------------------
# TEXT MODE — standard st.chat_input
# ---------------------------------------------------------------------------
else:
    if prompt := st.chat_input("Message Friday…"):
        # User bubble
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Friday bubble + streaming
        with st.chat_message("assistant"):
            response = stream_response(prompt)

        st.session_state.messages.append({"role": "assistant", "content": response})
