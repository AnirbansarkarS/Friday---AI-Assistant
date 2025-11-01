# frontend/pages/3_Settings.py
"""
Settings for model preferences
"""
import streamlit as st

st.title("⚙️ Model Settings")

st.selectbox("Select Model Backend", ["Hugging Face", "Ollama", "Local Model"])
st.slider("Response Temperature", 0.0, 1.0, 0.7)
st.text_input("API Key (if needed)")

st.success("Settings saved (session-based)")