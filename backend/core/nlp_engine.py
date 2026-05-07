def detect_mood(text):
    """
    Classify user message sentiment dynamically.
    Returns: sad, happy, anxious, or neutral
    """
    text = text.lower()
    
    happy_words = ["happy", "great", "awesome", "good", "excellent", "excited", "joy", "fun"]
    sad_words = ["sad", "depressed", "down", "terrible", "bad", "cry", "lonely", "unhappy"]
    anxious_words = ["anxious", "worried", "nervous", "stressed", "scared", "fear", "panic"]
    
    if any(word in text for word in sad_words):
        return "sad"
    elif any(word in text for word in happy_words):
        return "happy"
    elif any(word in text for word in anxious_words):
        return "anxious"
    
    return "neutral"

def interpret_command(text):
    text = text.lower()

    if "open" in text:
        return "open_app", "Opening application"
    elif "search" in text:
        return "search_web", "Searching the web"
    elif "hello" in text or "hi" in text:
        return "greet", "Hello Anirban, how can I help you today?"
    elif "exit" in text or "stop" in text:
        exit()
    else:
        return "unknown", "Sorry, I didn’t understand that."

