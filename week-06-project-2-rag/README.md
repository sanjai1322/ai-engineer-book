# Week 6 — Project 2: RAG (Retrieval-Augmented Generation)

**Book chapters:** 6.1–6.5

Your second project. Build a system that answers questions about a document by
finding relevant chunks and feeding them to the model as context. This is how
ChatGPT plugins, Notion AI, and most "chat with your docs" tools work.

## Files

| File | What it does |
|------|-------------|
| `rag.py` | Core RAG logic: `load()` chunks and embeds, `ask()` retrieves and answers |
| `app.py` | Streamlit app: upload documents, ask questions, see answers and sources |
| `sample_docs/handbook.txt` | A company handbook with deliberate gaps for testing refusals |
| `chunk_size_experiment.py` | Try different chunk sizes and see how results change |

## How to run

```bash
# Run the core logic directly
python week-06-project-2-rag/rag.py

# Or run the Streamlit app
streamlit run week-06-project-2-rag/app.py
```

## What you should see

- `rag.py` — Answers to three questions. The first two are answered from the handbook.
  The third ("What is the employee vacation policy?") should get a refusal because
  that information is not in the document.
- `app.py` — A web interface to upload documents and ask questions. Source chunks
  are shown in an expandable section.

## Testing the refusal path

The sample handbook deliberately does not cover employee policies, HR procedures,
or product specifications. Try asking questions about these topics to verify the
model says "I don't have enough information" instead of making things up.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `No API key found` | `.env` file missing or empty | Copy `.env.example` to `.env` and paste your key |
| `ModuleNotFoundError: No module named 'chromadb'` | ChromaDB not installed | Run `pip install -r requirements.txt` |
| Very slow embedding step | Each chunk makes an API call | Normal for large documents. Consider reducing chunk count. |
