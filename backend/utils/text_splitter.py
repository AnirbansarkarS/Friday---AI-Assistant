"""
Splits long text into smaller chunks for RAG
"""

def split_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks