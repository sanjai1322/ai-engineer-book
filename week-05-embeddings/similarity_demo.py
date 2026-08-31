"""
Similarity demo — §5.3–5.4.

Compare how similar different texts are to each other using cosine similarity.
Related texts score high, unrelated texts score low.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.embeddings import embed, similarity


def main():
    texts = [
        "How do I return a product?",
        "What is your return policy?",
        "I want to send this item back for a refund.",
        "What time does the store open?",
        "Tell me about your shipping options.",
    ]

    print("Embedding all texts...\n")
    vectors = [embed(t) for t in texts]

    # Compare every pair
    print("Similarity scores:")
    print("-" * 60)
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            score = similarity(vectors[i], vectors[j])
            print(f"  {score:.4f}  |  '{texts[i]}'")
            print(f"           |  '{texts[j]}'")
            print()


if __name__ == "__main__":
    main()
