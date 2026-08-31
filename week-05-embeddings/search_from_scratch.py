"""
Semantic search from scratch — §5.5.

Build a search engine using only embeddings and cosine similarity.
No database, no library — just vectors and math.

Note: the sort uses key=lambda x: x[0] to break ties cleanly.
Without this, Python raises TypeError when two scores are equal and it
tries to compare the text strings as a tiebreaker.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.embeddings import embed, similarity

# A small knowledge base to search through
DOCUMENTS = [
    "Our return policy allows returns within 30 days of purchase.",
    "Shipping takes 3-5 business days for standard delivery.",
    "We offer free shipping on orders over $50.",
    "Contact our support team at support@example.com for help.",
    "Our warranty covers manufacturing defects for one year.",
    "Gift cards can be purchased in denominations of $25, $50, and $100.",
    "International shipping is available to over 40 countries.",
    "Premium members get free express shipping on all orders.",
]


def find_closest(question, documents, doc_vectors, top=3):
    """Find the most similar documents to a query."""
    q = embed(question)
    
    scored = [(similarity(q, v), d)
              for v, d in zip(doc_vectors, documents)]
              
    # Sort on the score only. Without key=, Python compares the
    # document strings whenever two scores tie, and raises TypeError.
    scored.sort(key=lambda x: x[0], reverse=True)
    
    return scored[:top]


def main():
    print("Embedding documents...\n")
    # Pre-compute vectors for the documents
    doc_vectors = [embed(doc) for doc in DOCUMENTS]
    
    question = "How can I send something back?"
    print(f"Question: {question}\n")

    results = find_closest(question, DOCUMENTS, doc_vectors)

    print("Top results:")
    for score, doc in results:
        print(f"  {score:.4f}  {doc}")


if __name__ == "__main__":
    main()
