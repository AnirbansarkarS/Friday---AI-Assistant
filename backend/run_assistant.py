# run_assistant.py
from speech.speech_to_text import listen_for_command
from executor.TaskGenerator import generate_command
from executor.TaskExecutor import execute_command

WAKE_WORD = "hey friday"

def main():
    while True:
        query = listen_for_command()
        if WAKE_WORD in query:
            print("👋 Hey Anirban, I’m listening...")
            command = listen_for_command()
            code = generate_command(command)
            print("AI generated command:", code)
            result = execute_command(code)
            print(result)

if __name__ == "__main__":
    main()
