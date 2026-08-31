"""
Evaluation harness — §9.4.

Run your AI through a set of test cases and measure how well it performs.
This is how you know whether a change made things better or worse.

Each case has an input, an expected output (or outcome), and the eval
checks whether the actual output matches.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "week-06-project-2-rag"))

# Import ask from our week 6 RAG system
from rag import ask, load

def load_cases(path):
    """Load evaluation cases from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate(cases):
    """Run all cases and print a summary."""
    passed = 0
    print(f"Running {len(cases)} evaluation cases...\n")
    
    for c in cases:
        out, sources = ask(c["input"])
        out = out.lower()
        
        ok = all(t.lower() in out for t in c.get("must_contain", []))
        ok = ok and not any(
            t.lower() in out for t in c.get("must_not_contain", [])
        )
        
        if c.get("expect_refusal"):
            ok = "not covered" in out
            
        passed += int(ok)
        
        if not ok:
            print("FAIL:", c["input"])
            print("  Output was:", out[:100])
            print()
            
    print(f"{passed}/{len(cases)} passed")


def main():
    cases_path = os.path.join(os.path.dirname(__file__), "cases.example.json")

    if not os.path.exists(cases_path):
        print("No cases file found. Copy cases.example.json and add your test cases.")
        return

    # To run the evaluation, we need to make sure the handbook is loaded
    # into the RAG database.
    handbook_path = os.path.join(
        os.path.dirname(__file__), "..", "week-06-project-2-rag", "sample_docs", "handbook.txt"
    )
    if os.path.exists(handbook_path):
        with open(handbook_path, "r", encoding="utf-8") as f:
            load(f.read())
            
    cases = load_cases(cases_path)
    evaluate(cases)


if __name__ == "__main__":
    main()
