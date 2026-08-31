"""
Chunk size experiment — §6.3.

What happens when you change the chunk size? Smaller chunks are more focused
but lose context. Larger chunks keep more context but are less precise.

This script tries several chunk sizes on the same document and compares
how well the search works.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import chromadb
from shared.client import client
from shared.chunking import chunk_text
from shared.usage import log_usage


class OpenAIEmbeddingFunction:
    def __call__(self, input):
        results = []
        for text in input:
            response = client.embeddings.create(
                input=text,
                model="text-embedding-3-small",
            )
            log_usage(response, "text-embedding-3-small")
            results.append(response.data[0].embedding)
        return results


def test_chunk_size(text, question, chunk_size, overlap=50):
    """Load a document with a specific chunk size and search it."""
    chroma = chromadb.Client()
    name = f"chunks_{chunk_size}"

    collection = chroma.create_collection(
        name=name,
        embedding_function=OpenAIEmbeddingFunction(),
    )

    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )

    results = collection.query(query_texts=[question], n_results=1)
    top_chunk = results["documents"][0][0]
    distance = results["distances"][0][0]

    return len(chunks), top_chunk, distance


def main():
    sample_path = os.path.join(os.path.dirname(__file__), "sample_docs", "handbook.txt")

    if not os.path.exists(sample_path):
        print("No sample document found. Place handbook.txt in sample_docs/")
        return

    with open(sample_path, "r", encoding="utf-8") as f:
        text = f.read()

    question = "What is the return policy?"
    print(f"Question: {question}\n")

    for size in [200, 500, 1000, 2000]:
        num_chunks, top_chunk, distance = test_chunk_size(text, question, size)
        print(f"Chunk size: {size}")
        print(f"  Number of chunks: {num_chunks}")
        print(f"  Distance: {distance:.4f}")
        print(f"  Top chunk preview: {top_chunk[:100]}...")
        print()


if __name__ == "__main__":
    main()
