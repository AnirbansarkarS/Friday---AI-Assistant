# frontend/app.py
"""
Streamlit main UI app
"""
import streamlit as st
from helpers.api_client import APIClient

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

st.title("🤖 AI Assistant Dashboard")
st.sidebar.success("Select a page from the left")

client = APIClient()

st.write("Welcome to the AI Assistant! Navigate using the sidebar to start chatting or upload documents.")





