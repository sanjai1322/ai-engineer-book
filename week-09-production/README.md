# Week 9 — Production Readiness

**Book chapters:** 9.1–9.5

Before you deploy, you need to know: does it work? How much will it cost?
What could go wrong? This week's tools answer all three.

## Files

| File | What it does |
|------|-------------|
| `evaluate.py` | Run your AI through test cases and measure pass rate |
| `cases.example.json` | 30 evaluation cases covering accuracy, safety, tone, and edge cases |
| `cost_projection.py` | Estimate monthly cost at different traffic levels |
| `guardrails.py` | Input and output checks to catch injections and leaks |

## How to run

```bash
# From the repo root
python week-09-production/evaluate.py
python week-09-production/cost_projection.py
python week-09-production/guardrails.py
```

## What you should see

- `evaluate.py` — A pass/fail result for each of the 30 cases, with a summary score.
  Not all will pass on the first run; that is the point.
- `cost_projection.py` — A table showing projected costs across models and traffic levels.
  No API key needed — this is pure math.
- `guardrails.py` — Two inputs get blocked (injection attempts), two go through normally.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `No API key found` | `.env` file missing or empty | Copy `.env.example` to `.env` and paste your key |
| Low eval scores | Model behaviour varies with updates | Adjust expected values or grading method |
| `FileNotFoundError` on cases | Wrong working directory | Run from the repo root |
