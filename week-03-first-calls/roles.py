"""
System, user, and assistant roles — Chapter 3.

Shows how the system message shapes the model's behaviour without
changing the user's question.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.client import client
from shared.usage import log_usage


def ask(system, user):
    """Send a message with a system prompt and print the reply."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0,
    )
    print(response.choices[0].message.content)
    log_usage(response, "gpt-4o-mini")
    print()


def main():
    question = "What is the capital of France?"

    print("--- No system prompt ---")
    ask("", question)

    print("--- Pirate ---")
    ask("You are a pirate. Answer in pirate speak.", question)

    print("--- Concise expert ---")
    ask("You are a geography expert. Answer in exactly one word.", question)


if __name__ == "__main__":
    main()
