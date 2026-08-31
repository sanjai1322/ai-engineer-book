# Week 4 — Project 1: Notes Cleanup Tool

**Book chapters:** 4.1–4.5

Your first real project. A Streamlit app that takes messy, unstructured meeting
notes and produces clean summaries with action items.

## Files

| File | What it does |
|------|-------------|
| `notes_tool.py` | The Streamlit app — upload or paste notes, get a clean summary |
| `sample_notes/` | Five genuinely messy meeting notes to test with |

## How to run

```bash
# From the repo root
streamlit run week-04-project-1-notes-tool/notes_tool.py
```

This opens your browser. Upload one of the files from `sample_notes/` or paste
your own text.

## What you should see

- A text area for pasting notes and a file uploader
- After clicking "Clean up notes," a structured summary with decisions, action
  items, and open questions
- Token usage printed in the terminal

## Sample notes

| File | Tests |
|------|-------|
| `standup_call.txt` | Typos, informal language, missing owners |
| `q3_planning.txt` | Long, lots of detail, unresolved decisions |
| `client_call_empty.txt` | Nearly empty — should trigger a "not enough to summarize" response |
| `incident_retro.txt` | Technical incident with timeline and action items |
| `one_on_one.txt` | Personal 1-on-1 with half-sentences |

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `No API key found` | `.env` file missing or empty | Copy `.env.example` to `.env` and paste your key |
| `ModuleNotFoundError: No module named 'streamlit'` | Streamlit not installed | Run `pip install -r requirements.txt` |
| App opens but nothing happens on click | Button state issue | Refresh the page and try again |
