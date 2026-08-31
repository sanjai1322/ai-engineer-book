"""
Token estimator — Chapter 3.

Estimates how many tokens a message will use before sending it,
then compares to the actual usage reported by the API.

Rule of thumb: 1 token is roughly 4 characters in English.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.client import client
from shared.usage import log_usage


def estimate_tokens(text):
    """Rough estimate: 1 token per 4 characters."""
    return len(text) // 4


def main():
    message = (
        "Explain what an API is to a ten-year-old in three sentences. "
        "Use a simple analogy."
    )

    estimated = estimate_tokens(message)
    print(f"Input text: {len(message)} characters")
    print(f"Estimated tokens: ~{estimated}")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}],
        temperature=0,
    )

    actual_in = response.usage.prompt_tokens
    actual_out = response.usage.completion_tokens

    print(f"Actual input tokens: {actual_in}")
    print(f"Actual output tokens: {actual_out}")
    print(f"Estimation was off by: {abs(estimated - actual_in)} tokens")
    print()
    print("Response:")
    print(response.choices[0].message.content)
    log_usage(response, "gpt-4o-mini")


if __name__ == "__main__":
    main()
