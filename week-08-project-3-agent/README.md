# Week 8 — Project 3: Support Agent

**Book chapters:** 8.1–8.4

Your third project. A customer support agent that reads messages, looks up
policies and orders, drafts replies, and escalates to a human when needed.
This combines everything from weeks 5–7: embeddings, RAG, and tool calling.

## Files

| File | What it does |
|------|-------------|
| `tools.py` | Four tools: search_handbook, lookup_order, draft_reply, escalate |
| `triage.py` | The triage agent — reads a message, uses tools, responds or escalates |
| `app.py` | Streamlit review queue for testing messages |
| `test_messages.py` | 20 test messages with expected outcomes |

## How to run

```bash
# Run the triage agent directly
python week-08-project-3-agent/triage.py

# Or run the Streamlit review queue
streamlit run week-08-project-3-agent/app.py
```

## What you should see

- `triage.py` — Three test messages: a policy question (searches handbook), an order
  status query (looks up order), and a legal threat (escalates).
- `app.py` — A web interface with all 20 test messages. Click any message to run
  the agent and compare the result to the expected outcome.

## Test message categories

| Category | Count | What they test |
|----------|-------|---------------|
| Easy | 5 | Straightforward questions the agent should handle |
| Escalate | 5 | Must go to a human: legal threats, safety issues, supervisor requests |
| Ambiguous | 5 | Edge cases that test the agent's judgment |
| Hostile | 5 | Prompt injections, social engineering, angry customers |

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `No API key found` | `.env` file missing or empty | Copy `.env.example` to `.env` and paste your key |
| `Handbook not available` | Can't find `week-06-project-2-rag/sample_docs/handbook.txt` | Make sure you have week 6 files in place |
| Agent reveals system prompt | Prompt injection succeeded | Check system prompt wording in `triage.py` |
