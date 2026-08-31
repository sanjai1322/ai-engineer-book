# Week 11 — Flagship Project Starter

Which files to lift from which week to build your own project.

## The idea

Your flagship project combines everything you have learned: API calls, RAG,
tool calling, an agent loop, evaluation, and deployment. The specific
application is yours to choose, but the architecture is the same.

## Files to copy

| From | File | What you get |
|------|------|-------------|
| `shared/client.py` | `client.py` | API key loading and client setup |
| `shared/llm.py` | `llm.py` | The `complete()` wrapper |
| `shared/usage.py` | `usage.py` | Token and cost logging |
| `shared/embeddings.py` | `embeddings.py` | Embedding and similarity |
| `shared/chunking.py` | `chunking.py` | Text chunking for RAG |
| `week-06-project-2-rag/rag.py` | `rag.py` | Document loading and retrieval |
| `week-07-tools/agent_loop.py` | Reference | The agent loop pattern |
| `week-08-project-3-agent/tools.py` | Reference | How to define AVAILABLE and TOOL_SCHEMAS |
| `week-09-production/guardrails.py` | `guardrails.py` | Input/output safety checks |
| `week-10-deployment/auth_password.py` | Reference | Password protection for your deployed app |
| `week-10-deployment/rate_limit.py` | `rate_limit.py` | Rate limiting |

## How to start

1. Create a new folder for your project
2. Copy the files from the table above
3. Open `app.py` in this folder — it has TODO blocks marking where to add your code
4. Define your own tools in a new `tools.py`
5. Write your system prompt
6. Build the Streamlit interface
7. Add evaluation cases
8. Deploy

## Project ideas

- **Research assistant** — RAG over academic papers, summarize findings
- **Code reviewer** — Paste code, get feedback on style and bugs
- **Recipe finder** — RAG over a recipe database, suggest meals based on ingredients
- **Study buddy** — Upload lecture notes, quiz yourself with generated questions
- **Customer FAQ bot** — RAG over your company's docs, answer customer questions

The architecture is identical for all of these. The only differences are the
documents you load, the tools you write, and the system prompt.
