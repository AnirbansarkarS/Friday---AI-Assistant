# frontend/pages/chatbot.py
"""
Chatbot interface page
"""
import streamlit as st
import sys
import os

# Add root directory to path to allow imports from helpers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.api_client import APIClient

st.title("?? Chatbot (Friday)")
client = APIClient()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display chat messages from history on app rerun
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Talk to Friday..."):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Format history to send to API
    history_to_send = st.session_state.chat_history[:-1]

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream response
        for chunk in client.chat_stream(prompt, history=history_to_send):
            full_response += chunk
            message_placeholder.markdown(full_response + "¦")
            
        message_placeholder.markdown(full_response)
        
    # Add assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})
