# frontend/pages/1_Chatbot.py
"""
Chatbot interface page
"""
import streamlit as st
from helpers.api_client import APIClient

st.title("💬 Chatbot")
client = APIClient()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Type your message:")

if st.button("Send") and user_input:
    response = client.chat(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("AI", response))

for role, msg in st.session_state.chat_history:
    st.write(f"**{role}:** {msg}")