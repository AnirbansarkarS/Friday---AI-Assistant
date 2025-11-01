

# frontend/pages/2_Upload_Doc_RAG.py
"""
Upload document and ask questions using RAG
"""
import streamlit as st
from helpers.api_client import APIClient

st.title("📄 Document Q&A (RAG)")
client = APIClient()

uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])
if uploaded_file is not None:
    if st.button("Upload & Index"):
        result = client.upload_doc(uploaded_file)
        st.success(result)

question = st.text_input("Ask a question from the document:")
if st.button("Ask") and question:
    answer = client.ask_doc(question)
    st.write(f"**Answer:** {answer}")
