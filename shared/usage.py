"""
Token usage logging and cost estimation.

The book's central habit: print token usage and estimated cost after every
API call, one line. This module does the math so every script can call
log_usage(response) and get a consistent output.
"""

# Pricing per 1M tokens as of mid-2025 — update if OpenAI changes pricing.
# The book uses these same numbers.
COST_PER_1M = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4": {"input": 30.00, "output": 60.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "text-embedding-3-small": {"input": 0.02, "output": 0.00},
    "text-embedding-3-large": {"input": 0.13, "output": 0.00},
}


def estimate_cost(input_tokens, output_tokens, model="gpt-4o-mini"):
    """Return estimated cost in dollars for a single API call."""
    rates = COST_PER_1M.get(model, COST_PER_1M["gpt-4o-mini"])
    input_cost = (input_tokens / 1_000_000) * rates["input"]
    output_cost = (output_tokens / 1_000_000) * rates["output"]
    return input_cost + output_cost


def log_usage(response, model="gpt-4o-mini"):
    """Print a one-line usage summary. Works with both chat and embedding responses."""
    usage = response.usage

    if usage is None:
        print("  [usage] No usage data returned.")
        return

    input_tokens = usage.prompt_tokens
    output_tokens = getattr(usage, "completion_tokens", 0) or 0
    total = usage.total_tokens
    cost = estimate_cost(input_tokens, output_tokens, model)

    print(
        f"  [usage] {input_tokens} in + {output_tokens} out = {total} tokens"
        f"  (${cost:.6f})"
    )
