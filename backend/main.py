from core.speech_listener import listen_command
from core.nlp_engine import interpret_command
from core.task_executor import execute_task
from core.tts_engine import speak

def main():
    speak("Friday online. How can I help you Boss ?...")

    while True:
        command = listen_command()
        if not command:
            continue
        print(f"🗣️ You said: {command}")

        intent, response = interpret_command(command)
        execute_task(intent, command)
        speak(response)

if __name__ == "__main__":
    main()