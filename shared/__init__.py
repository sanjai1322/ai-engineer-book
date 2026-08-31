"""
Shared utilities for the AI Engineer companion code.

Provides the building blocks every chapter reuses:
- client: a configured OpenAI client that loads your .env
- complete: a single wrapper for chat completions
- embed / similarity: embedding and cosine similarity helpers
- chunk_text: text chunking for RAG
- log_usage: token and cost reporting
"""

from shared.client import get_client
from shared.llm import complete
from shared.embeddings import embed, similarity
from shared.chunking import chunk_text
from shared.usage import log_usage
