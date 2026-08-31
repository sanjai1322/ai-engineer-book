"""
Support Agent Streamlit App — Project 3.

A review queue for customer support messages. The agent triages each
message, and you can review the results.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from triage import triage
from test_messages import TEST_MESSAGES


def main():
    st.set_page_config(page_title="Support Agent — Review Queue", page_icon="🎧")
    st.title("Support Agent — Review Queue")
    st.write("Review how the agent handles customer messages. Click any message to see the agent's response.")

    # Message input
    tab1, tab2 = st.tabs(["Test Messages", "Custom Message"])

    with tab1:
        st.write("Select a test message to see how the agent handles it:")
        for i, msg in enumerate(TEST_MESSAGES):
            label = msg["category"].upper()
            with st.expander(f"[{label}] {msg['message'][:80]}..."):
                st.write(f"**Expected:** {msg['expected']}")
                if st.button(f"Run agent", key=f"run_{i}"):
                    with st.spinner("Agent is working..."):
                        result = triage(msg["message"])
                    st.subheader("Agent response")
                    st.json(result)

    with tab2:
        custom = st.text_area("Enter a customer message")
        if st.button("Run agent", disabled=not custom):
            with st.spinner("Agent is working..."):
                result = triage(custom)
            st.subheader("Agent response")
            st.json(result)


if __name__ == "__main__":
    print(
        "This is a Streamlit app. Run it with:\n"
        "  streamlit run week-08-project-3-agent/app.py"
    )
