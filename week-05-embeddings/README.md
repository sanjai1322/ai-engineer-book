# Week 5 — Embeddings

**Book chapters:** 5.1–5.6

Turn text into numbers so a computer can measure meaning. By the end of this
folder you will have built a semantic search engine from scratch, then rebuilt
it with ChromaDB.

## Files

| File | What it does |
|------|-------------|
| `make_embedding.py` | Create your first embedding and see the raw vector |
| `similarity_demo.py` | Compare cosine similarity between related and unrelated texts |
| `search_from_scratch.py` | Semantic search using only vectors and math — no database |
| `search_with_chroma.py` | The same search using ChromaDB to manage embeddings |

## How to run

```bash
# From the repo root
python week-05-embeddings/make_embedding.py
python week-05-embeddings/similarity_demo.py
python week-05-embeddings/search_from_scratch.py
python week-05-embeddings/search_with_chroma.py
```

## What you should see

- `make_embedding.py` — A 1536-dimensional vector. The first and last 10 values printed.
- `similarity_demo.py` — Scores near 0.9 for related texts ("return a product" vs "return policy"), scores near 0.5 for unrelated texts.
- `search_from_scratch.py` — The return policy document ranked first for "How can I send something back?"
- `search_with_chroma.py` — Same results, but using ChromaDB distances.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `No API key found` | `.env` file missing or empty | Copy `.env.example` to `.env` and paste your key |
| `ModuleNotFoundError: No module named 'chromadb'` | ChromaDB not installed | Run `pip install -r requirements.txt` |
| `TypeError` in sort | Using the old version without the sort fix | Make sure `find_closest` uses `key=lambda x: x[0]` in the sort |
