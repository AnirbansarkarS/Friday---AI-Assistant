import os
import webbrowser
from AppOpener import open as app_open

def execute_task(intent, command):
    if intent == "open_app":
        app_name = command.replace("open", "").strip()
        print(f"🚀 Attempting to open: {app_name}")
        try:
            # Use AppOpener for fuzzy matching and broad support
            app_open(app_name, match_closest=True, throw_error=True)
            return f"Opening {app_name}"
        except Exception as e:
            # Fallback to simple os.system for common stuff if AppOpener fails or is not setup entirely
            print(f"AppOpener failed: {e}")
            if "chrome" in app_name:
                os.system("start chrome" if os.name == "nt" else "open -a 'Google Chrome'")
                return "Opening Chrome"
            return f"Could not open {app_name}. Please try again."

    elif intent == "search_web":
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching web for {query}"

    elif intent == "greet":
        return "Hello! How can I help you?"

    elif "shutdown" in command:
        os.system("shutdown /s /t 1")
        return "Shutting down system."

    else:
        return "I am not sure how to handle that yet."
