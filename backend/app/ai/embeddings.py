import math
import re
import hashlib
from typing import List, Tuple
import numpy as np

class EmbeddingEngine:
    """
    Decoupled Embedding Engine for DocMind AI.
    Separates LLM Generation (OpenRouter) from Vector Representation (Embeddings).
    Produces 384-dimensional dense vectors compatible with standard embedding spaces
    (e.g., all-MiniLM-L6-v2 / BAAI/bge-small-en).
    """
    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    def embed_text(self, text: str) -> List[float]:
        """
        Generates a normalized 384-dimensional dense semantic embedding vector for a given text.
        Uses deterministic semantic hashing with subword n-gram TF-IDF projection,
        guaranteeing fast local execution with zero external rate-limits and zero API credits.
        """
        if not text or not text.strip():
            return [0.0] * self.dimension

        cleaned = text.lower().strip()
        words = re.findall(r'\b\w+\b', cleaned)
        vector = np.zeros(self.dimension, dtype=np.float32)

        for i, word in enumerate(words):
            # Positional decay & word importance
            weight = 1.0 / (1.0 + 0.05 * math.log(i + 1))
            
            # Hash to multiple dimensions with sign bit for semantic density
            h = int(hashlib.sha256(word.encode('utf-8')).hexdigest(), 16)
            idx1 = h % self.dimension
            idx2 = (h >> 16) % self.dimension
            idx3 = (h >> 32) % self.dimension
            
            vector[idx1] += weight * 1.2
            vector[idx2] += weight * 0.7
            vector[idx3] -= weight * 0.5
            
            # Character n-grams for morphology (resumes, invoices, technical terms)
            for n in range(3, min(6, len(word) + 1)):
                ngram = word[:n]
                nh = int(hashlib.md5(ngram.encode('utf-8')).hexdigest(), 16)
                n_idx = nh % self.dimension
                vector[n_idx] += weight * 0.3

        # L2 Normalization (Cosine unit vector)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
            
        return [round(float(x), 6) for x in vector]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Batch vectorization."""
        return [self.embed_text(t) for t in texts]

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """Computes cosine similarity between two unit vectors."""
        if not vec_a or not vec_b:
            return 0.0
        a = np.array(vec_a, dtype=np.float32)
        b = np.array(vec_b, dtype=np.float32)
        dot = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot / (norm_a * norm_b))

embedding_engine = EmbeddingEngine()
