from __future__ import annotations

import streamlit as st

from src.auth import authenticate_user


st.set_page_config(page_title="Login", layout="centered")


def render_login_form() -> None:
    st.markdown("## 🔐 Login")
    st.markdown("Please sign in to access the dashboards.")

    with st.form("login_form", clear_on_submit=False):
        identifier = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In")

        if submitted:
            user = authenticate_user(identifier, password)
            if user:
                st.session_state.auth_user = user
                try:
                    st.switch_page("app.py")
                except Exception:
                    st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")


def main() -> None:
    if st.session_state.get("auth_user"):
        try:
            st.switch_page("app.py")
        except Exception:
            st.rerun()
        return

    render_login_form()


if __name__ == "__main__":
    main()


