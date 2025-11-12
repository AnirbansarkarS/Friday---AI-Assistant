# backend/executor/TaskExecutor.py
import os, webbrowser

def execute_command(code):
    try:
        print(f"🧩 Executing: {code}")
        exec(code, {"os": os, "webbrowser": webbrowser})
        return "✅ Task executed successfully"
    except Exception as e:
        return f"❌ Error: {str(e)}"
