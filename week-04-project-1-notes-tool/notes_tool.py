"""
Notes Cleanup Tool — Project 1 (Chapter 4, §4.4).

A Streamlit app that takes messy meeting notes and produces clean,
structured summaries. Upload a text file or paste notes directly.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from shared.client import client
from shared.usage import log_usage

SYSTEM_PROMPT = """You are a meeting notes assistant. You take raw, messy
meeting notes and produce a clean summary with:
- A one-line summary of the meeting
- Key decisions made
- Action items with owners (if mentioned)
- Open questions

If the notes are too short or unclear to summarize, say so honestly."""


def process(notes):
    """Clean up messy meeting notes and return a structured summary."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": notes},
        ],
        temperature=0,
    )
    log_usage(response, "gpt-4o-mini")
    return response.choices[0].message.content


def main():
    st.set_page_config(page_title="Notes Cleanup Tool", page_icon="📝")
    st.title("Notes Cleanup Tool")
    st.write("Paste messy meeting notes or upload a text file. Get a clean summary.")

    # File upload
    uploaded = st.file_uploader("Upload a .txt file", type=["txt"])
    if uploaded:
        notes = uploaded.read().decode("utf-8")
        st.text_area("Uploaded notes", notes, height=200, disabled=True)
    else:
        notes = st.text_area("Or paste your notes here", height=200)

    if st.button("Clean up notes", disabled=not notes):
        with st.spinner("Processing..."):
            try:
                summary = process(notes)
                st.subheader("Cleaned Summary")
                st.markdown(summary)
            except Exception as e:
                st.error(f"Something went wrong: {e}")


if __name__ == "__main__":
    # Running directly with python shows a hint instead of crashing
    print(
        "This is a Streamlit app. Run it with:\n"
        "  streamlit run week-04-project-1-notes-tool/notes_tool.py"
    )
