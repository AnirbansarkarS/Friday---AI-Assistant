import streamlit as st
from helpers.api_client import APIClient

# Page Config
st.set_page_config(page_title="Friday AI", page_icon="🤖", layout="wide")

# Custom CSS for chat interface
st.markdown("""
<style>
    .stChatInput {
        position: fixed;
        bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize API Client
client = APIClient()

# Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("Friday AI")
    st.write("Your personal assistant.")
    if st.button("🎤 Listen"):
        with st.spinner("Listening..."):
            command = client.listen()
            if command:
                # Add user message to state
                st.session_state.messages.append({"role": "user", "content": command})
                # Get response
                response = client.chat(command)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
            else:
                st.error("Could not understand audio.")
                
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main Chat Interface
st.title("🤖 Chat with Friday")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("What is your command?"):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat(prompt)
            st.markdown(response)
    
    # Add assistant message to state
    st.session_state.messages.append({"role": "assistant", "content": response})
