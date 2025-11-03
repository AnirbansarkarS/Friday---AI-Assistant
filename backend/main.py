
from core.speech_listener import listen_command
from core.nlp_engine import interpret_command
from core.task_executor import execute_task
from core.tts_engine import speak

def main():
    speak("Friday online. Listening for your command...")

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
# from fastapi import FastAPI
# from .routes import health, chat, rag
# from .config import HOST, PORT
# import os


# app = FastAPI()


# app.include_router(health.router, prefix="/api")
# app.include_router(chat.router, prefix="/api")
# app.include_router(rag.router, prefix="/api")


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("backend.app:app", host=HOST, port=PORT, reload=True)
