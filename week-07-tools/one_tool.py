"""
One tool — §7.2.

The simplest tool-calling example: give the model a single function
and let it decide when to call it.

Distinguishes AVAILABLE (name -> Python callable) from TOOL_SCHEMAS
(JSON sent to the model). The model sees the schema, your code calls
the function from AVAILABLE.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.client import client
from shared.usage import log_usage


# --- The tool ---

def get_weather(city):
    """Fake weather lookup. In a real app, this would call a weather API."""
    weather = {
        "London": "15°C, cloudy",
        "Tokyo": "28°C, sunny",
        "New York": "22°C, partly cloudy",
    }
    return weather.get(city, f"No weather data for {city}")


# AVAILABLE maps function names to the actual Python callables
AVAILABLE = {
    "get_weather": get_weather,
}

# TOOL_SCHEMAS is what the model sees — the JSON description of each tool
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name, e.g. 'London'",
                    }
                },
                "required": ["city"],
            },
        },
    }
]


def main():
    question = "What's the weather in Tokyo?"
    print(f"User: {question}\n")

    # Step 1: Ask the model, giving it the tool schemas
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}],
        tools=TOOL_SCHEMAS,
        temperature=0,
    )
    log_usage(response, "gpt-4o-mini")

    message = response.choices[0].message

    # Step 2: If the model wants to call a tool, call it
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        fn_name = tool_call.function.name
        fn_args = json.loads(tool_call.function.arguments)

        print(f"Model wants to call: {fn_name}({fn_args})")

        # Look up the function in AVAILABLE and call it
        fn = AVAILABLE[fn_name]
        result = fn(**fn_args)
        print(f"Tool returned: {result}")

        # Step 3: Send the result back to the model
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": question},
                message,
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                },
            ],
            temperature=0,
        )
        log_usage(response, "gpt-4o-mini")

        print(f"\nAssistant: {response.choices[0].message.content}")
    else:
        print(f"Assistant: {message.content}")


if __name__ == "__main__":
    main()
