"""
RAG Streamlit App — Project 2.

Upload a document (or use the sample handbook), ask questions, and see the
answer along with the source chunks the model used.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from rag import load, ask


def main():
    st.set_page_config(page_title="RAG — Ask Your Documents", page_icon="📄")
    st.title("RAG — Ask Your Documents")
    st.write(
        "Upload a document or use the sample handbook. "
        "Ask questions and get answers grounded in the text."
    )

    # Document loading
    if "loaded" not in st.session_state:
        st.session_state.loaded = False

    col1, col2 = st.columns(2)

    with col1:
        uploaded = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded and st.button("Load uploaded file"):
            text = uploaded.read().decode("utf-8")
            with st.spinner("Chunking and embedding..."):
                load(text)
                st.session_state.loaded = True
            st.success(f"Loaded {len(text)} characters")

    with col2:
        sample_path = os.path.join(os.path.dirname(__file__), "sample_docs", "handbook.txt")
        if os.path.exists(sample_path):
            if st.button("Load sample handbook"):
                with open(sample_path, "r", encoding="utf-8") as f:
                    text = f.read()
                with st.spinner("Chunking and embedding..."):
                    load(text)
                    st.session_state.loaded = True
                st.success(f"Loaded sample handbook ({len(text)} characters)")

    # Question answering
    st.divider()

    if not st.session_state.loaded:
        st.info("Load a document first, then ask questions below.")
        return

    question = st.text_input("Ask a question about the document")

    if question:
        with st.spinner("Searching and generating answer..."):
            answer, sources = ask(question)

        st.subheader("Answer")
        st.markdown(answer)

        with st.expander("Source chunks used"):
            for i, chunk in enumerate(sources):
                st.markdown(f"**Chunk {i + 1}:**")
                st.text(chunk)
                st.divider()


if __name__ == "__main__":
    print(
        "This is a Streamlit app. Run it with:\n"
        "  streamlit run week-06-project-2-rag/app.py"
    )
