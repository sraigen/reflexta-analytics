from __future__ import annotations

"""Simple authentication helpers that use the existing `users` table.

This module is intentionally minimal and non-invasive:
- It only reads from the database via Streamlit connections
- It stores a small `auth_user` object in `st.session_state`
- Pages can call `require_login()` to enforce authentication
"""

from typing import Optional, Dict, Any

import streamlit as st


def _get_sql_conn():
    """Return the configured Streamlit SQL connection."""
    return st.connection("sql", type="sql")


def _safe_get(row: Dict[str, Any], *names: str) -> Optional[Any]:
    for name in names:
        if name in row and row[name] is not None:
            return row[name]
    return None


def authenticate_user(identifier: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate using the existing `users` table.

    Identifier can be username or email. Supports either plaintext passwords
    or hashed passwords (bcrypt). Returns a minimal user dict on success.
    """

    identifier = (identifier or "").strip()
    password = password or ""
    if not identifier or not password:
        return None

    try:
        conn = _get_sql_conn()
        df = conn.query(
            """
            SELECT *
            FROM users
            WHERE username = :ident OR email = :ident
            LIMIT 1
            """,
            params={"ident": identifier},
        )
        if df is None or df.empty:
            return None

        row = df.iloc[0].to_dict()

        # Detect password columns
        stored_hash = _safe_get(row, "password_hash", "hashed_password")
        stored_plain = _safe_get(row, "password")

        is_valid = False
        if stored_hash:
            try:
                import bcrypt  # lazy import

                if isinstance(stored_hash, str):
                    stored_hash_bytes = stored_hash.encode("utf-8")
                else:
                    stored_hash_bytes = stored_hash
                is_valid = bcrypt.checkpw(password.encode("utf-8"), stored_hash_bytes)
            except Exception:
                is_valid = False
        elif stored_plain is not None:
            is_valid = str(stored_plain) == password

        if not is_valid:
            return None

        user = {
            "id": _safe_get(row, "id", "user_id"),
            "username": _safe_get(row, "username") or identifier,
            "email": _safe_get(row, "email"),
            "role": _safe_get(row, "role", "user_role"),
        }
        return user
    except Exception:
        return None


def require_login() -> None:
    """Redirect to the login page if not authenticated."""
    if "auth_user" not in st.session_state or not st.session_state.get("auth_user"):
        try:
            st.switch_page("pages/00_Login.py")
        except Exception:
            st.stop()


def logout() -> None:
    st.session_state.pop("auth_user", None)
    st.session_state.pop("sidebar_chat_history", None)
    st.rerun()


