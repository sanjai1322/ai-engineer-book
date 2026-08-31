"""
Your first API call — Chapter 3.

This is the "Hello, World" of AI engineering. Run it to confirm
your API key works and you can talk to the model.
"""

import sys
import os

# Add the repo root to the path so we can import shared/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.client import client
from shared.usage import log_usage


def main():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Say hello in one sentence."}
        ],
        temperature=0,
    )

    print(response.choices[0].message.content)
    log_usage(response, "gpt-4o-mini")


if __name__ == "__main__":
    main()
