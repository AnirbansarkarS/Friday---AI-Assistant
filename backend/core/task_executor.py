import os
import webbrowser

def execute_task(intent, command):
    if intent == "open_app":
        if "chrome" in command:
            os.system("start chrome" if os.name == "nt" else "open -a 'Google Chrome'")
        elif "word" in command:
            os.system("start winword" if os.name == "nt" else "open -a 'Microsoft Word'")
        else:
            print("⚠️ App not recognized.")

    elif intent == "search_web":
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif intent == "greet":
        print("👋 Hello there!")

    else:
        print("Command not mapped.")
