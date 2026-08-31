"""
Load environment variables and return a configured OpenAI client.

This is the first thing the book sets up (Chapter 3). Every script imports
from here so there is exactly one place to manage the API key.
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


def get_client():
    """Return an OpenAI client, or exit with a helpful message if no key."""

    # Walk up from the calling script to find the .env file at the repo root.
    # This lets scripts in any week folder find the same .env.
    here = Path(__file__).resolve().parent
    repo_root = here.parent
    load_dotenv(repo_root / ".env")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print(
            "\n  No API key found.\n"
            "  Copy .env.example to .env and paste your OpenAI key after the '=' sign.\n"
            "  You can get a key at https://platform.openai.com/api-keys\n"
        )
        sys.exit(1)

    return OpenAI(api_key=api_key)


# Module-level convenience — most scripts just do `from shared.client import client`.
# Lazy: the client is created the first time it is used, not on import.
# This lets modules like chunking.py be imported without an API key.
_client = None


def _get_lazy_client():
    global _client
    if _client is None:
        _client = get_client()
    return _client


class _LazyClient:
    """Proxy that creates the real client on first attribute access."""

    def __getattr__(self, name):
        return getattr(_get_lazy_client(), name)


client = _LazyClient()
