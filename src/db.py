from __future__ import annotations

"""Database connection helpers for Streamlit app.

Uses Streamlit's connection API. Configure the SQLAlchemy URL in `.streamlit/secrets.toml`.
"""

from typing import Any

import streamlit as st


def get_conn() -> Any:
    """Return a Streamlit SQL connection named "sql".

    The connection is configured via `[connections.sql]` in `.streamlit/secrets.toml`.
    """

    return st.connection("sql", type="sql")


def health_check() -> bool:
    """Run a minimal query to verify database connectivity.

    Returns True if the query succeeds, otherwise logs an error and returns False.
    """

    try:
        conn = get_conn()
        # SELECT 1 works for PostgreSQL and Oracle
        _ = conn.query("SELECT 1 AS ok")
        return True
    except Exception as exc:  # noqa: BLE001
        st.error(f"Database health check failed: {exc}")
        return False


