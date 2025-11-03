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
