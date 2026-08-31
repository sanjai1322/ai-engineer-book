"""
Embedding and similarity helpers — §5.3 and §5.4.

embed() turns text into a vector.
similarity() compares two vectors using cosine similarity.
"""

import numpy as np
from shared.client import client
from shared.usage import log_usage


def embed(text, model="text-embedding-3-small"):
    """Return the embedding vector for a piece of text."""
    response = client.embeddings.create(
        input=text,
        model=model,
    )
    log_usage(response, model)
    return response.data[0].embedding


def similarity(a, b):
    """Cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
