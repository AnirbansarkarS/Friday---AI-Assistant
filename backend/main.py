from fastapi import FastAPI
from pydantic import BaseModel
from backend.core.speech_listener import listen_command
from backend.core.nlp_engine import interpret_command
from backend.core.task_executor import execute_task
from backend.core.tts_engine import speak
from backend.routes.chat import router as chat_router

app = FastAPI()

app.include_router(chat_router)

class BasicChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Friday AI Backend Online"}

@app.get("/listen")
def listen_endpoint():
    """
    Triggers the server-side microphone to listen for a command.
    """
    command = listen_command()
    if command:
        intent = interpret_command(command)
        response = execute_task(intent)
        speak(response)
        return {"command": command, "intent": intent, "response": response}
    return {"error": "Could not understand"}
