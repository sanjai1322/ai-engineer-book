"""
Temperature comparison — Chapter 3.

Same prompt, two temperatures. Temperature 0 is nearly deterministic.
Temperature 1 gives creative, varied responses.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.client import client
from shared.usage import log_usage

PROMPT = "Give me a one-sentence startup idea."


def generate(temperature, runs=3):
    """Generate the same prompt multiple times at a given temperature."""
    print(f"\n--- Temperature {temperature} ---")
    for i in range(runs):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": PROMPT}],
            temperature=temperature,
        )
        print(f"  Run {i + 1}: {response.choices[0].message.content}")
        log_usage(response, "gpt-4o-mini")


def main():
    generate(temperature=0)
    generate(temperature=1)


if __name__ == "__main__":
    main()
