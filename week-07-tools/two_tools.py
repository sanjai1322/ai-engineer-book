"""
Two tools — §7.3.

Give the model two tools and let it pick the right one based on the question.
Same AVAILABLE / TOOL_SCHEMAS pattern as one_tool.py.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.client import client
from shared.usage import log_usage


# --- Tools ---

def get_weather(city):
    """Fake weather lookup."""
    weather = {
        "London": "15°C, cloudy",
        "Tokyo": "28°C, sunny",
        "New York": "22°C, partly cloudy",
    }
    return weather.get(city, f"No weather data for {city}")


def get_time(city):
    """Fake time lookup."""
    times = {
        "London": "3:00 PM GMT",
        "Tokyo": "11:00 PM JST",
        "New York": "10:00 AM EST",
    }
    return times.get(city, f"No time data for {city}")


AVAILABLE = {
    "get_weather": get_weather,
    "get_time": get_time,
}

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
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current local time for a city.",
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
    },
]


def call_with_tools(question):
    """Ask a question that might require tools, then handle the response."""
    print(f"User: {question}")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}],
        tools=TOOL_SCHEMAS,
        temperature=0,
    )
    log_usage(response, "gpt-4o-mini")

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        fn_name = tool_call.function.name
        fn_args = json.loads(tool_call.function.arguments)

        print(f"  -> Calling {fn_name}({fn_args})")

        fn = AVAILABLE[fn_name]
        result = fn(**fn_args)
        print(f"  -> Result: {result}")

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

        print(f"Assistant: {response.choices[0].message.content}\n")
    else:
        print(f"Assistant: {message.content}\n")


def main():
    call_with_tools("What's the weather in London?")
    call_with_tools("What time is it in Tokyo?")
    call_with_tools("What is 2 + 2?")  # Should not call any tool


if __name__ == "__main__":
    main()
