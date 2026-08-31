"""
Single wrapper for chat completions — see Appendix B.

Every script in the book calls complete() instead of hitting the API directly.
This keeps the interface consistent and ensures usage is always logged.
"""

from shared.client import client
from shared.usage import log_usage


def complete(prompt, system="", model="gpt-4o-mini", temperature=0, tools=None):
    """
    Send a chat completion request and return the response.

    Args:
        prompt:      The user message (string).
        system:      Optional system message (string).
        model:       Model name. Default: gpt-4o-mini.
        temperature: Sampling temperature. Default: 0 (deterministic).
        tools:       Optional list of tool schemas for function calling.

    Returns:
        The full API response object.
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    if tools:
        kwargs["tools"] = tools

    response = client.chat.completions.create(**kwargs)
    log_usage(response, model)

    return response
