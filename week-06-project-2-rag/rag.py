"""
RAG — Retrieval-Augmented Generation — §6.4.

load() reads a document, chunks it, and stores the chunks in ChromaDB.
ask() takes a question, finds relevant chunks, and sends them to the model
as context.

This is the core of Project 2. The Streamlit app in app.py wraps this.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import chromadb
from chromadb.utils import embedding_functions
from shared.client import client
from shared.chunking import chunk_text
from shared.usage import log_usage

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

# Module-level globals matching the book's structure on page 65
db = chromadb.Client().create_collection("docs", embedding_function=openai_ef)


def load(text):
    """Chunk a document and store it in ChromaDB."""
    chunks = chunk_text(text)
    print(f"  Split into {len(chunks)} chunks")

    db.add(
        documents=chunks,
        ids=[f"c{i}" for i in range(len(chunks))]
    )
    print(f"  Stored {len(chunks)} chunks in ChromaDB")


SYSTEM = """Answer using ONLY the provided context.
If the context does not contain the answer, reply exactly:
"That is not covered in the documents I have."
Never use outside knowledge. Quote the relevant line where possible."""


def ask(question):
    """Find relevant chunks and ask the model to answer based on them."""
    hits = db.query(query_texts=[question], n_results=4)
    context = "\n\n---\n\n".join(hits["documents"][0])
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", 
             "content": f"CONTEXT:\n{context}\n\nQUESTION: {question}"}
        ]
    )
    log_usage(response, "gpt-4o-mini")

    return response.choices[0].message.content, hits["documents"][0]


def main():
    # Quick demo using the sample handbook
    sample_path = os.path.join(os.path.dirname(__file__), "sample_docs", "handbook.txt")

    if not os.path.exists(sample_path):
        print("No sample document found. Place handbook.txt in sample_docs/")
        return

    with open(sample_path, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"Loaded document: {len(text)} characters")
    load(text)

    questions = [
        "What is the return policy?",
        "How do I contact support?",
        "What is the employee vacation policy?",  # Not in the handbook — tests refusal
    ]

    for q in questions:
        print(f"\nQ: {q}")
        answer, sources = ask(q)
        print(f"A: {answer}")
        print(f"  (based on {len(sources)} chunks)")


if __name__ == "__main__":
    main()
