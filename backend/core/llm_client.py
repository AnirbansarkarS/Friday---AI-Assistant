# backend/executor/TaskGenerator.py
from core.llm_client import ask_ai

def generate_command(query):
    prompt = f"""
    You are a system assistant. Convert this request into a valid Python OS command or function call.
    Example:
    - "open chrome" → "os.startfile('chrome')"
    - "open ms word" → "os.startfile('winword')"
    - "search cat pictures" → "webbrowser.open('https://www.google.com/search?q=cat+pictures')"

    Now generate the command for: {query}
    Return only the Python code to execute.
    """
    return ask_ai(prompt)
