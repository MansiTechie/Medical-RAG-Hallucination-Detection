"""
Retrieval service — FAISS vector search.

Loads the pre-built FAISS index + metadata produced by
scripts/build_index.py and provides similarity search.
"""

import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import settings


class RetrievalService:
    def __init__(self):
        self.embedding_model = None
        self.index = None
        self.metadata = []
        self.embeddings = None  # stored for verification service

    def load_models_and_index(self):
        """Load embedding model and FAISS index at startup."""
        print(f"Loading embedding model: {settings.EMBEDDING_MODEL_NAME}")
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

        index_path = os.path.join(settings.VECTOR_DB_PATH, "index.faiss")
        metadata_path = os.path.join(settings.VECTOR_DB_PATH, "metadata.json")

        if os.path.exists(index_path) and os.path.exists(metadata_path):
            print(f"Loading FAISS index: {index_path}")
            self.index = faiss.read_index(index_path)

            print(f"Loading metadata: {metadata_path}")
            with open(metadata_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

            print(f"Loaded {self.index.ntotal} vectors.")

            # Re-encode chunks to have embeddings available for verification
            print("Encoding chunks for verification service...")
            texts = [chunk["text"] for chunk in self.metadata]
            self.embeddings = self.embedding_model.encode(
                texts, show_progress_bar=True
            ).astype("float32")
            print(f"Embeddings shape: {self.embeddings.shape}")

        else:
            print(
                "WARNING: FAISS index or metadata not found. "
                "Run scripts/build_index.py first."
            )

    def search(self, query: str, top_k: int = 5) -> list:
        """Search the FAISS index for the most relevant chunks."""
        if not self.index or not self.embedding_model:
            raise RuntimeError("Retrieval models/index not loaded.")

        query_embedding = self.embedding_model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, k=top_k)

        results = []
        for rank, idx in enumerate(indices[0]):
            if 0 <= idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results


retrieval_service = RetrievalService()
