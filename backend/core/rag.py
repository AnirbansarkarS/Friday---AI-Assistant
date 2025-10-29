"""
RAG = retrieve + generate pipeline
"""
import numpy as np
from .embeddings import Embeddings

class RAG:
    def __init__(self, inference_pipeline, vector_store):
        self.pipe = inference_pipeline
        self.db = vector_store
        self.embedder = Embeddings()

    def query(self, user_query):
        query_embedding = self.embedder.encode([user_query])[0]
        docs = self.db.similarity_search(query_embedding)
        context = "
".join(docs)
        prompt = f"Context: {context}

Question: {user_query}
Answer:"
        return self.pipe.generate(prompt)
