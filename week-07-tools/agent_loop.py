"""
Agent loop — §7.4.

A loop that lets the model call tools repeatedly until it has enough
information to answer, or until max_steps is reached. This is the
simplest version of an agent.

Full logging shows every step so you can see the model's reasoning.
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
        "Paris": "18°C, light rain",
    }
    return weather.get(city, f"No weather data for {city}")


def get_time(city):
    """Fake time lookup."""
    times = {
        "London": "3:00 PM GMT",
        "Tokyo": "11:00 PM JST",
        "New York": "10:00 AM EST",
        "Paris": "4:00 PM CET",
    }
    return times.get(city, f"No time data for {city}")


def compare_weather(city_a, city_b):
    """Compare weather between two cities."""
    w_a = get_weather(city_a)
    w_b = get_weather(city_b)
    return f"{city_a}: {w_a} | {city_b}: {w_b}"


AVAILABLE = {
    "get_weather": get_weather,
    "get_time": get_time,
    "compare_weather": compare_weather,
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
                    "city": {"type": "string", "description": "The city name"},
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
                    "city": {"type": "string", "description": "The city name"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_weather",
            "description": "Compare the weather between two cities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_a": {"type": "string", "description": "First city"},
                    "city_b": {"type": "string", "description": "Second city"},
                },
                "required": ["city_a", "city_b"],
            },
        },
    },
]


def agent(question, max_steps=5):
    """Run the agent loop: ask, call tools, repeat until done or max_steps."""
    print(f"User: {question}\n")

    messages = [{"role": "user", "content": question}]

    for step in range(1, max_steps + 1):
        print(f"--- Step {step} ---")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOL_SCHEMAS,
            temperature=0,
        )
        log_usage(response, "gpt-4o-mini")

        message = response.choices[0].message

        # If no tool calls, the model is done
        if not message.tool_calls:
            print(f"  Model is done.\n")
            print(f"Assistant: {message.content}")
            return message.content

        # Process each tool call
        messages.append(message)

        for tool_call in message.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)

            print(f"  Calling {fn_name}({fn_args})")

            fn = AVAILABLE[fn_name]
            result = fn(**fn_args)

            print(f"  Result: {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

    print(f"\n  Reached max_steps ({max_steps}). Stopping.")
    return "I was not able to complete the task in the allowed steps."


def main():
    # Simple question — one tool call
    agent("What's the weather in Paris?")

    print("\n" + "=" * 60 + "\n")

    # Complex question — might need multiple tool calls
    agent("Compare the weather in London and Tokyo, and tell me what time it is in both cities.")


if __name__ == "__main__":
    main()
