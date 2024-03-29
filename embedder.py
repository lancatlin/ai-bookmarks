from sentence_transformers import SentenceTransformer
import numpy as np

from bookmark_manager import BookmarkManager


class Embedder:
    def __init__(self, model="all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(model)

    def embed(self, sentences):
        embeddings = self.embedder.encode(sentences)
        return embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
