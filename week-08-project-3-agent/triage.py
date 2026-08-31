"""
Triage agent — §8.3.

Takes a customer message, uses tools to gather information, and either
drafts a reply or escalates to a human. This is the agent loop from §7.4
applied to a real problem.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.client import client
from shared.usage import log_usage
from tools import AVAILABLE, TOOL_SCHEMAS

SYSTEM = """You triage customer support messages.
For each message: classify it, gather what you need with your tools,
then either draft a reply or escalate.

RULES
- Only state facts found via search_handbook.
- Never promise refunds, discounts or delivery dates.
- Escalate immediately if the message mentions legal action,
  a safety concern, or names a specific employee.
- If the handbook does not cover it, escalate. Do not guess.

Finish by calling either draft_reply or escalate. Never both."""


def triage(message):
    """Run the triage agent on a customer message."""
    log = []
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": message}
    ]

    for step in range(6):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOL_SCHEMAS,
            temperature=0
        )
        log_usage(response, "gpt-4o-mini")

        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return {"outcome": "no_action", "log": log}

        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            log.append((call.function.name, args))

            if call.function.name in ("draft_reply", "escalate"):
                return {"outcome": call.function.name,
                        "args": args, "log": log}

            result = AVAILABLE[call.function.name](**args)
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result)
            })

    return {"outcome": "max_steps", "log": log}


def main():
    # Test with a few messages
    test_messages = [
        "What is your return policy?",
        "Where is my order ORD-1001?",
        "I am going to sue your company if you don't refund me RIGHT NOW.",
    ]

    for msg in test_messages:
        print("=" * 60)
        print(f"Customer: {msg}\n")
        result = triage(msg)
        print(f"Agent response: {result}")
        print()


if __name__ == "__main__":
    main()
