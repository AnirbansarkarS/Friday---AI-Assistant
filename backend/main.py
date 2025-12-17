from fastapi import FastAPI
from pydantic import BaseModel
from core.speech_listener import listen_command
from core.nlp_engine import interpret_command
from core.task_executor import execute_task
from core.tts_engine import speak

app = FastAPI()

class ChatRequest(BaseModel):
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
        # Interpret and execute immediately? Or just return the text?
        # Let's return the text so frontend sees what was heard, then frontend calls /chat
        return {"command": command}
    else:
        return {"command": None, "error": "Could not understand audio"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    command = request.message
    print(f"📩 Received command: {command}")
    
    intent, response_text = interpret_command(command)
    
    # If the intent implies an action (like opening an app), execute it
    if intent != "unknown" and intent != "greet":
        execution_result = execute_task(intent, command)
        if execution_result:
            response_text = f"{response_text}. {execution_result}"
    
    # Optional: Speak the response on the server side? 
    # Maybe limit this to only when voice was used? 
    # For now, let's keep it simple and just return text. 
    # If users want the bot to talk, we can add a flag.
    # speak(response_text) 
    
    return {"response": response_text, "intent": intent}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
