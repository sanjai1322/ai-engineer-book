"""
Vague description — §7.3.

A bad tool description, then the fix. This demonstrates why the text you
put in tool descriptions matters as much as the code itself.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.client import client
from shared.usage import log_usage


def lookup_order(order_id):
    """Fake order lookup."""
    orders = {
        "ORD-001": "Shipped, arrives Thursday",
        "ORD-002": "Processing, ships tomorrow",
        "ORD-003": "Delivered on Monday",
    }
    return orders.get(order_id, f"Order {order_id} not found")


# --- Bad version: vague description ---

BAD_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": "Does stuff with orders.",  # Too vague
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The ID",  # Unhelpful
                    }
                },
                "required": ["order_id"],
            },
        },
    }
]

# --- Good version: clear, specific description ---

GOOD_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": "Look up the current status and delivery estimate for a customer order by its order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, formatted as 'ORD-XXX', e.g. 'ORD-001'",
                    }
                },
                "required": ["order_id"],
            },
        },
    }
]


def test_schema(label, schema, question):
    """Try a question with a given schema and see if the model calls the tool."""
    print(f"\n--- {label} ---")
    print(f"User: {question}")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}],
        tools=schema,
        temperature=0,
    )
    log_usage(response, "gpt-4o-mini")

    message = response.choices[0].message
    if message.tool_calls:
        tc = message.tool_calls[0]
        args = json.loads(tc.function.arguments)
        print(f"  Model called: {tc.function.name}({args})")
    else:
        print(f"  Model did NOT call the tool")
        print(f"  Instead said: {message.content}")


def main():
    question = "Where is my order ORD-001?"

    test_schema("Bad description", BAD_SCHEMA, question)
    test_schema("Good description", GOOD_SCHEMA, question)


if __name__ == "__main__":
    main()
