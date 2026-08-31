# Week 11 — Flagship Project

**Book chapters:** 11.1–11.3

Your capstone project. This is where you combine everything — API calls, RAG,
tool calling, evaluation, and deployment — into one application that you design.

## Files

| File | What it does |
|------|-------------|
| `STARTER.md` | Which files to copy from which week |
| `app.py` | Skeleton app with marked TODO blocks |

## How to start

1. Read `STARTER.md` to understand which building blocks you need
2. Open `app.py` and look for the four TODO sections
3. Define your tools, write your system prompt, build your UI
4. Test with the evaluation harness from week 9
5. Deploy using the guide from week 10

## The TODO blocks in app.py

| TODO | What to do |
|------|-----------|
| TODO 1 | Define your tools (AVAILABLE + TOOL_SCHEMAS) |
| TODO 2 | Write your system prompt |
| TODO 3 | Build the Streamlit interface |
| TODO 4 | Add sidebar controls |

## How to run

```bash
# The skeleton runs as-is — it just doesn't do anything useful yet
streamlit run week-11-flagship/app.py
```

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `No API key found` | `.env` file missing or empty | Copy `.env.example` to `.env` and paste your key |
| `KeyError` on tool call | Tool name in TOOL_SCHEMAS doesn't match AVAILABLE | Make sure the names are identical |
| Agent loops forever | No exit condition in tools | Add logic that returns a final answer |
