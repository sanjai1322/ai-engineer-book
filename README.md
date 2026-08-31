# AI Engineer — Companion Code

Learn AI engineering from scratch — build RAG systems, AI agents with tool calling, and evaluation pipelines using only Python and the OpenAI API.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
[![Book on Gumroad](https://img.shields.io/badge/Book-on%20Gumroad-ff90e8?logo=gumroad&logoColor=white)](https://store.codeconstellation.com/ai-engineer)

## What You Will Build

| Week | Project | What it does |
|------|---------|-------------|
| 4 | **Notes Cleanup Tool** | Upload messy meeting notes → get clean summaries with action items |
| 6 | **RAG Q&A System** | Chat with your documents using retrieval-augmented generation |
| 8 | **Support Agent** | An AI agent that searches policies, looks up orders, drafts replies, and escalates |
| 11 | **Flagship App** | Your own project combining everything — RAG, tools, eval, deployment |

<!-- Screenshots will go here once available
![Notes Tool](docs/images/notes-tool.png)
![RAG App](docs/images/rag-app.png)
![Support Agent](docs/images/support-agent.png)
-->

## Quickstart

```bash
git clone https://github.com/sanjai1322/ai-engineer-book.git
cd ai-engineer-book
pip install -r requirements.txt
cp .env.example .env   # Then paste your OpenAI API key after the = sign
```

Get your API key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

## Cost

Running every script in this repo end to end costs roughly **$2–4** in API
credits. Most of that is the embedding-heavy RAG examples. The week 3 scripts
cost fractions of a cent.

## Chapter → Folder

| Chapters | Folder | Topic |
|----------|--------|-------|
| 3 | `week-03-first-calls/` | First API calls, roles, temperature |
| 4 | `week-04-project-1-notes-tool/` | **Project 1:** Notes cleanup tool |
| 5 | `week-05-embeddings/` | Embeddings, similarity, semantic search |
| 6 | `week-06-project-2-rag/` | **Project 2:** RAG — ask your documents |
| 7 | `week-07-tools/` | Tool calling and the agent loop |
| 8 | `week-08-project-3-agent/` | **Project 3:** Customer support agent |
| 9 | `week-09-production/` | Evaluation, cost projection, guardrails |
| 10 | `week-10-deployment/` | Deployment, auth, rate limiting |
| 11 | `week-11-flagship/` | **Flagship:** Your own project |

## How to Use This Repo

**Type the code from the book first.** Use these files to compare against when
you are stuck. The learning happens in the typing, the debugging, and the
moments where something does not work and you figure out why.

Do not clone this repo and skip ahead. You will end up with working code and no
understanding of how it works.

Each folder has its own README with:
- Which chapter it covers
- What each file does
- How to run it
- What you should see
- The three most likely errors and how to fix them

## What This Is Not

This is not a framework. It is not a library. It is not production-ready as-is.

This is companion code for a book that teaches the primitives of AI engineering.
Every file is deliberately simple. There are no abstractions, no classes where a
function will do, no LangChain, no LlamaIndex. If you want to understand what
those tools do under the hood, this is where you start.

## The Book

**AI Engineer — Build and ship 4 real AI products in 12 weeks** by Sanjai K
(Code Constellation).

A twelve-week course for people who have never written a line of code. You will
build four real projects, understand how they work at every level, and deploy
one to the internet.

📖 [Get the book on Gumroad](https://codeconstellation.gumroad.com/l/juipx)

📄 [Read Chapter 1 free](ai-engineer-chapter-1-free.pdf)

## Limitations

- **API dependency.** Every script that calls a model requires an OpenAI API key
  and an internet connection. If OpenAI changes their API, some scripts may need
  updates.
- **Model behaviour changes.** GPT-4o-mini's outputs are not frozen. Evaluation
  scores, exact wording, and tool-calling decisions may shift with model updates.
- **Not production code.** Error handling is minimal. Rate limiting is in-memory.
  Auth is password-based. These are teaching examples, not templates for
  production systems.
- **Cost.** While cheap ($2–4 total), these scripts do make real API calls that
  cost real money. Set a spending limit at
  [platform.openai.com/account/billing](https://platform.openai.com/account/billing).

## Security

- Never commit your `.env` file. It is in `.gitignore` by default.
- Before pushing, scan your history: `git log --all -p | grep -i "sk-"`
- If you find a leaked key, revoke it immediately at
  [platform.openai.com/api-keys](https://platform.openai.com/api-keys) and
  rotate.

## License

MIT — see [LICENSE](LICENSE).
