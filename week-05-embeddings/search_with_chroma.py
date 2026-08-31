"""
Semantic search with ChromaDB — §5.6.

The same search as search_from_scratch.py, but using ChromaDB to store and
query embeddings. This is what you would use in a real project.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import chromadb
from chromadb.utils import embedding_functions

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


def main():
    # Pass the OpenAI embedding function so ChromaDB uses the correct model.
    # Without this, Chroma silently downloads a local model and the results
    # will not match the ones from search_from_scratch.py.
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )

    # Create an in-memory ChromaDB client
    chroma = chromadb.Client()
    collection = chroma.create_collection(
        name="documents",
        embedding_function=openai_ef,
    )

    # Add documents
    print("Adding documents to ChromaDB...")
    collection.add(
        documents=DOCUMENTS,
        ids=[f"doc_{i}" for i in range(len(DOCUMENTS))],
    )

    # Search
    query = "How can I send something back?"
    print(f"\nQuery: {query}\n")

    results = collection.query(
        query_texts=[query],
        n_results=3,
    )

    print("Top results:")
    for doc, distance in zip(results["documents"][0], results["distances"][0]):
        # ChromaDB returns distances (lower = more similar)
        print(f"  {distance:.4f}  {doc}")


if __name__ == "__main__":
    main()
