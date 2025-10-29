"""
Local vector database using ChromaDB
"""
import chromadb
from chromadb.config import Settings

class ChromaDB:
    def __init__(self, persist_dir="./data/vectorstore"):
        self.client = chromadb.Client(
            Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_dir)
        )
        self.collection = self.client.get_or_create_collection("documents")

    def add_documents(self, docs, embeddings):
        ids = [f"doc_{i}" for i in range(len(docs))]
        self.collection.add(documents=docs, embeddings=embeddings.tolist(), ids=ids)

    def similarity_search(self, query_embedding, n_results=3):
        results = self.collection.query(query_embeddings=[query_embedding], n_results=n_results)
        return results["documents"][0]