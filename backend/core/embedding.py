from sentence_transformers import SentenceTransformer
from ..config import EMBEDDING_MODEL

_embed_model = None


def get_embedding_model():
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embed_model


def embed_texts(texts):
    model = get_embedding_model()
    return model.encode(texts, show_progress_bar=False, convert_to_numpy=True)