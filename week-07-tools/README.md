# Week 7 — Tool Calling

**Book chapters:** 7.1–7.4

Teach the model to use tools. Instead of making up answers, the model calls
your Python functions — weather lookups, database queries, anything you write.
By the end you will have a working agent loop.

## Files

| File | What it does |
|------|-------------|
| `one_tool.py` | Simplest tool-calling example: one function, one call |
| `two_tools.py` | Two tools — the model picks the right one |
| `vague_description.py` | Bad tool description vs good one — see the difference |
| `agent_loop.py` | A loop: ask, call tools, repeat until done (§7.4) |

## Key concept: AVAILABLE vs TOOL_SCHEMAS

Every file in this folder separates two things:

- **`AVAILABLE`** — a dict mapping function names to Python callables. Your code uses this to actually run the function.
- **`TOOL_SCHEMAS`** — a list of JSON schemas describing the tools. The model sees this and decides what to call.

The model never runs your code directly. It outputs a function name and arguments as JSON. You look up the function in `AVAILABLE`, call it, and send the result back.

## How to run

```bash
# From the repo root
python week-07-tools/one_tool.py
python week-07-tools/two_tools.py
python week-07-tools/vague_description.py
python week-07-tools/agent_loop.py
```

## What you should see

- `one_tool.py` — The model calls `get_weather("Tokyo")` and reports "28°C, sunny"
- `two_tools.py` — Weather question calls `get_weather`, time question calls `get_time`, math question calls nothing
- `vague_description.py` — Bad description may fail; good description works
- `agent_loop.py` — Step-by-step log of the model calling tools and building an answer

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `No API key found` | `.env` file missing or empty | Copy `.env.example` to `.env` and paste your key |
| `KeyError` on tool name | Model returned a function name not in `AVAILABLE` | Check that `AVAILABLE` keys match `TOOL_SCHEMAS` function names |
| `json.JSONDecodeError` | Model returned malformed arguments | Rare with gpt-4o-mini, retry usually fixes it |
