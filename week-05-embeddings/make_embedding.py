"""
Make your first embedding — §5.2.

An embedding is a list of numbers that captures the meaning of text.
This script embeds a sentence and shows what the vector looks like.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.embeddings import embed


def main():
    text = "The cat sat on the mat."

    print(f"Text: {text}")
    print(f"Creating embedding...")

    vector = embed(text)

    print(f"Dimensions: {len(vector)}")
    print(f"First 10 values: {vector[:10]}")
    print(f"Last 10 values: {vector[-10:]}")


if __name__ == "__main__":
    main()
