"""
Cost projection — §9.3.

Estimate what your AI product will cost to run at scale.
Takes your average token usage per request and projects monthly cost
at different traffic levels.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.usage import COST_PER_1M


def project_cost(avg_input_tokens, avg_output_tokens, requests_per_day, model="gpt-4o-mini"):
    """Project monthly cost based on average usage and traffic."""
    rates = COST_PER_1M.get(model, COST_PER_1M["gpt-4o-mini"])

    daily_input_tokens = avg_input_tokens * requests_per_day
    daily_output_tokens = avg_output_tokens * requests_per_day

    daily_cost = (
        (daily_input_tokens / 1_000_000) * rates["input"]
        + (daily_output_tokens / 1_000_000) * rates["output"]
    )

    monthly_cost = daily_cost * 30
    return daily_cost, monthly_cost


def main():
    # Typical values from the book's support agent
    avg_input = 800   # tokens per request (system prompt + user message + tool results)
    avg_output = 200  # tokens per response

    print("Cost Projection")
    print("=" * 60)
    print(f"Average input tokens per request:  {avg_input}")
    print(f"Average output tokens per request: {avg_output}")
    print()

    models = ["gpt-4o-mini", "gpt-4o", "gpt-4"]
    traffic_levels = [100, 1000, 10000, 100000]

    for model in models:
        print(f"\n--- {model} ---")
        print(f"  {'Requests/day':<15} {'Daily':<12} {'Monthly':<12}")
        print(f"  {'-' * 39}")

        for rpd in traffic_levels:
            daily, monthly = project_cost(avg_input, avg_output, rpd, model)
            print(f"  {rpd:<15,} ${daily:<11.2f} ${monthly:<11.2f}")


if __name__ == "__main__":
    main()
