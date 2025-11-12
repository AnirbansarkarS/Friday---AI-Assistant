# backend/speech/speech_to_text.py
import speech_recognition as sr

def listen_for_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            print(f"You said: {query}")
            return query.lower()
        except:
            return ""
