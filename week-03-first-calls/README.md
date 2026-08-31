# Week 3 — First API Calls

**Book chapters:** 3.1–3.5

Your first conversation with an AI model. By the end of this folder you will
have made API calls, understood roles, experimented with temperature, and
learned to estimate costs before you spend.

## Files

| File | What it does |
|------|-------------|
| `first_call.py` | Your very first API call — confirm your key works |
| `roles.py` | System, user, and assistant roles change the model's behaviour |
| `temperature_demo.py` | Temperature 0 (deterministic) vs 1 (creative) |
| `token_estimator.py` | Estimate tokens before sending, compare to actual |

## How to run

```bash
# From the repo root
python week-03-first-calls/first_call.py
python week-03-first-calls/roles.py
python week-03-first-calls/temperature_demo.py
python week-03-first-calls/token_estimator.py
```

## What you should see

- `first_call.py` — A one-sentence greeting, plus a usage line showing tokens and cost.
- `roles.py` — Three different answers to "What is the capital of France?" depending on the system prompt.
- `temperature_demo.py` — Three nearly identical answers at temperature 0, three varied answers at temperature 1.
- `token_estimator.py` — An estimate, the actual count, and how far off the estimate was.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `No API key found` | `.env` file missing or empty | Copy `.env.example` to `.env` and paste your key |
| `openai.AuthenticationError` | Invalid API key | Check your key at https://platform.openai.com/api-keys |
| `ModuleNotFoundError: No module named 'openai'` | Dependencies not installed | Run `pip install -r requirements.txt` from the repo root |
