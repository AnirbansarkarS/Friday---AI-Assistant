"""
NLP Engine for Friday AI — Intent Classifier
Classifies user text into actionable intents with entity extraction.
"""

import re
from typing import Tuple

# ---------------------------------------------------------------------------
# Intent patterns
# ---------------------------------------------------------------------------

_OPEN_PATTERNS = [
    r"(?:open|launch|start|run|execute)\s+(.+)",
]

_SEARCH_PATTERNS = [
    r"(?:search(?:\s+for)?|look(?:\s+up)?|find|google|bing)\s+(.+)",
    r"(?:what is|who is|tell me about)\s+(.+)",
]

_SYSTEM_PATTERNS = [
    r"(shutdown|restart|reboot|volume\s+up|volume\s+down|mute|sleep)",
]

_GREET_PATTERNS = [
    r"^(?:hi|hello|hey|howdy|good\s+(?:morning|afternoon|evening))",
]


def _match_first(patterns: list, text: str) -> str | None:
    """Return the first captured group from the first matching pattern, or None."""
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return m.group(1).strip() if m.lastindex else text.strip()
    return None


def classify_intent(text: str) -> Tuple[str, str]:
    """
    Classify a user utterance into (intent, entity).

    Intents:
        open_app       — launch an application
        search_web     — search the web for a query
        system_control — OS-level commands
        greet          — greeting
        chat           — general conversation (route to LLM)

    Returns:
        (intent: str, entity: str)  — entity is the extracted noun/query
    """
    text = text.strip()

    entity = _match_first(_OPEN_PATTERNS, text)
    if entity:
        return "open_app", entity

    entity = _match_first(_SEARCH_PATTERNS, text)
    if entity:
        return "search_web", entity

    entity = _match_first(_SYSTEM_PATTERNS, text)
    if entity:
        return "system_control", entity

    entity = _match_first(_GREET_PATTERNS, text)
    if entity is not None:
        return "greet", ""

    return "chat", text


# ---------------------------------------------------------------------------
# Legacy helpers (kept for backwards compatibility)
# ---------------------------------------------------------------------------

def detect_mood(text: str) -> str:
    """Classify user message sentiment. Returns: sad | happy | anxious | neutral"""
    text = text.lower()
    if any(w in text for w in ["sad", "depressed", "down", "terrible", "bad", "cry", "lonely", "unhappy"]):
        return "sad"
    if any(w in text for w in ["happy", "great", "awesome", "good", "excellent", "excited", "joy", "fun"]):
        return "happy"
    if any(w in text for w in ["anxious", "worried", "nervous", "stressed", "scared", "fear", "panic"]):
        return "anxious"
    return "neutral"


def interpret_command(text: str) -> Tuple[str, str]:
    """Alias for classify_intent (backwards compatibility)."""
    return classify_intent(text)


# ---------------------------------------------------------------------------
# Standalone test — run:  python -m backend.core.nlp_engine
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    tests = [
        "open notepad",
        "launch spotify",
        "search for Python tutorials",
        "what is the capital of France",
        "google best pizza near me",
        "shutdown",
        "volume up",
        "hello Friday",
        "I am feeling a bit sad today",
        "Can you help me write a poem?",
    ]
    print("=== Intent Classifier Test ===\n")
    for t in tests:
        intent, entity = classify_intent(t)
        mood = detect_mood(t)
        print(f"  Input : {t!r}")
        print(f"  Intent: {intent}  |  Entity: {entity!r}  |  Mood: {mood}")
        print()
