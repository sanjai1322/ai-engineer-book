"""
Flagship Project — Skeleton App.

This is a starting point for your own project. The TODO blocks mark
where you need to add your own code. Everything else is wired up
and ready to go.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from shared.client import client
from shared.usage import log_usage
from shared.chunking import chunk_text


# =============================================================================
# TODO 1: Define your tools
#
# Create your own tools following the pattern from week 8.
# Each tool is a Python function. AVAILABLE maps names to callables.
# TOOL_SCHEMAS describes each tool in JSON for the model.
# =============================================================================

def example_tool(query):
    """Replace this with your own tool."""
    return f"You searched for: {query}"


AVAILABLE = {
    "example_tool": example_tool,
    # TODO: Add your tools here
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "example_tool",
            "description": "An example tool. Replace this with your own.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    }
                },
                "required": ["query"],
            },
        },
    },
    # TODO: Add your tool schemas here
]


# =============================================================================
# TODO 2: Write your system prompt
#
# This is the most important part. It defines what your agent does,
# what rules it follows, and how it behaves.
# =============================================================================

SYSTEM_PROMPT = """You are a helpful assistant.

TODO: Replace this with your own system prompt. Be specific about:
- What the assistant's job is
- What tools it should use and when
- What it should never do
- How it should handle edge cases
"""


# =============================================================================
# Agent loop — reused from week 7
# =============================================================================

def agent(messages, max_steps=5):
    """Run the agent loop until done or max_steps."""
    for step in range(1, max_steps + 1):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOL_SCHEMAS,
            temperature=0,
        )
        log_usage(response, "gpt-4o-mini")

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append(message)

        for tool_call in message.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)

            fn = AVAILABLE.get(fn_name)
            if fn is None:
                result = f"Unknown tool: {fn_name}"
            else:
                result = fn(**fn_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

    return "I was unable to complete the request in the allowed steps."


# =============================================================================
# TODO 3: Build your Streamlit interface
# =============================================================================

def main():
    st.set_page_config(page_title="My AI App", page_icon="🚀")
    st.title("My AI App")
    st.write("TODO: Replace this with your app description.")

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        elif msg["role"] == "assistant":
            st.chat_message("assistant").write(msg["content"])

    # User input
    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        # Build messages for the API
        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        api_messages.extend(st.session_state.messages)

        with st.spinner("Thinking..."):
            response = agent(api_messages)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

    # =============================================================================
    # TODO 4: Add a sidebar with controls, document upload, or settings
    # =============================================================================
    with st.sidebar:
        st.write("TODO: Add sidebar controls here")
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    print(
        "This is a Streamlit app. Run it with:\n"
        "  streamlit run week-11-flagship/app.py"
    )
