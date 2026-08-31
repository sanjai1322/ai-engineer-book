"""
Password authentication for Streamlit — Chapter 10.

Add a simple password gate to your Streamlit app so only people
with the password can use it. Not production security, but enough
to keep random visitors from running up your API bill.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st


def check_password():
    """Return True if the user has entered the correct password."""

    # In production, store this in Streamlit secrets or environment variables.
    # Never hardcode a real password.
    correct_password = os.environ.get("APP_PASSWORD", "demo")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    password = st.text_input("Enter password to continue", type="password")

    if password:
        if password == correct_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    return False


def main():
    st.set_page_config(page_title="Protected App", page_icon="🔒")
    st.title("Protected App")

    if not check_password():
        st.stop()

    # Everything below this line is protected
    st.success("You're in! This content is behind the password gate.")
    st.write(
        "In your real app, replace this section with your actual app code. "
        "Import `check_password` from this file and call it at the top of your app."
    )


if __name__ == "__main__":
    print(
        "This is a Streamlit app. Run it with:\n"
        "  streamlit run week-10-deployment/auth_password.py"
    )
