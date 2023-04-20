import os
from difflib import SequenceMatcher
from typing import Any, List

import numpy as np
import openai


def similarity(text1: str, text2: str) -> float:
    """Calculate the similarity between two texts."""
    return SequenceMatcher(None, text1, text2).ratio()

def similarity_ada(text1: str, text2: str) -> float:
    """Calculate the similarity between two texts using OpenAI ada embedding."""
    batch = [text1, text2]
    response: Any = openai.Embedding.create(
        model="text-embedding-ada-002",
        api_key=os.environ.get('OPENAI_API_KEY'),
        input=batch,
    )
    embs: List[List[float]] = [e["embedding"] for e in response["data"]]
    return calc_cosine_similarity(embs[0], embs[1])


def calc_cosine_similarity(emb1: List[float], emb2: List[float]) -> float:
    """Calculate the cosine similarity between two embeddings."""
    return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
