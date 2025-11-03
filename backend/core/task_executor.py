import os
import subprocess
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
    elif "shutdown" in command:
        os.system("shutdown /s /t 1")
        return "Shutting down system."

    else:
        print("Command not mapped.")

    

# def execute_task(command):
#     command = command.lower()



#     elif "open chrome" in command:
#         os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
#         return "Opening Google Chrome."

#     elif "search youtube" in command:
#         query = command.replace("search youtube for", "").strip()
#         webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
#         return f"Searching YouTube for {query}."



#     else:
#         return "Sorry, I don't know that command yet."
