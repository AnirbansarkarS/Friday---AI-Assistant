"""
Friday AI — Document Upload & RAG Management Page
Upload PDFs or text files. View and delete indexed documents.
"""

import os
import streamlit as st
import requests

BACKEND_URL = os.getenv("FRIDAY_BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Friday — Knowledge Base", page_icon="📚", layout="centered")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("📚 Friday's Knowledge Base")
st.caption("Upload documents so Friday can reference them in conversations.")
st.divider()

# ---------------------------------------------------------------------------
# Upload Section
# ---------------------------------------------------------------------------
st.subheader("➕ Add a Document")

uploaded = st.file_uploader(
    "Drag & drop a PDF or TXT file",
    type=["pdf", "txt", "md"],
    help="Supported: PDF, plain text (.txt), Markdown (.md)",
)

if uploaded is not None:
    if st.button("📤 Upload & Index", type="primary", use_container_width=True):
        with st.spinner(f"Ingesting **{uploaded.name}**… this may take a moment."):
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/rag/upload",
                    files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)},
                    timeout=120,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.success(
                        f"✅ **{data['doc_name']}** indexed successfully — "
                        f"{data['chunks']} chunks stored."
                    )
                    st.balloons()
                else:
                    st.error(f"❌ Upload failed: {resp.json().get('detail', resp.text)}")
            except requests.exceptions.ConnectionError:
                st.error("⚠️ Cannot reach Friday's backend. Make sure the server is running.")
            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")

st.divider()

# ---------------------------------------------------------------------------
# Indexed Documents Section
# ---------------------------------------------------------------------------
st.subheader("📂 Indexed Documents")

col_refresh, _ = st.columns([1, 4])
with col_refresh:
    refresh = st.button("🔄 Refresh List")

@st.cache_data(ttl=10)
def fetch_docs():
    try:
        resp = requests.get(f"{BACKEND_URL}/rag/docs", timeout=10)
        resp.raise_for_status()
        return resp.json().get("docs", [])
    except Exception:
        return None

if refresh:
    st.cache_data.clear()

docs = fetch_docs()

if docs is None:
    st.warning("⚠️ Could not fetch document list. Is the backend running?")
elif len(docs) == 0:
    st.info("No documents indexed yet. Upload one above!")
else:
    st.markdown(f"**{len(docs)} document(s) in Friday's knowledge base:**")
    for doc_name in docs:
        col_name, col_del = st.columns([5, 1])
        with col_name:
            st.markdown(f"📄 `{doc_name}`")
        with col_del:
            if st.button("🗑️", key=f"del_{doc_name}", help=f"Delete {doc_name}"):
                with st.spinner(f"Removing **{doc_name}**…"):
                    try:
                        del_resp = requests.delete(
                            f"{BACKEND_URL}/rag/docs/{requests.utils.quote(doc_name, safe='')}",
                            timeout=15,
                        )
                        if del_resp.status_code == 200:
                            data = del_resp.json()
                            st.success(
                                f"🗑️ Removed **{doc_name}** "
                                f"({data['chunks_deleted']} chunks deleted)."
                            )
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Error: {del_resp.json().get('detail', del_resp.text)}")
                    except Exception as e:
                        st.error(f"⚠️ {e}")
