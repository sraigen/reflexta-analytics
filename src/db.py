from __future__ import annotations

"""Database connection helpers for Streamlit app.

Uses Streamlit's connection API. Configure the SQLAlchemy URL in `.streamlit/secrets.toml`.
"""

import os
from typing import Any

import streamlit as st


def get_conn() -> Any:
    """Return a Streamlit SQL connection named "sql".

    The connection is configured via `[connections.sql]` in `.streamlit/secrets.toml`.
    For Streamlit Cloud, we force the Supabase URL to avoid localhost issues.
    """

    # Force Supabase URL for Streamlit Cloud to avoid localhost connection issues
    # Use environment variable for security, fallback to working credentials
    SUPABASE_URL = os.getenv("SUPABASE_URL", "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres")
    
    try:
        # Try to use the forced Supabase URL first
        return st.connection("sql", type="sql", url=SUPABASE_URL)
    except Exception:
        # Fallback to secrets-based connection for local development
        return st.connection("sql", type="sql")


def health_check() -> bool:
    """Run a minimal query to verify database connectivity.

    Returns True if the query succeeds, otherwise logs an error and returns False.
    """

    try:
        conn = get_conn()
        if conn is None:
            st.error("Database connection failed: Missing SQL DB connection configuration. Did you forget to set this in secrets.toml or as kwargs to st.connection?")
            return False
        # SELECT 1 works for PostgreSQL and Oracle
        _ = conn.query("SELECT 1 AS ok")
        return True
    except Exception as exc:  # noqa: BLE001
        st.error(f"Database health check failed: {exc}")
        st.info("Please check your database configuration in Streamlit Cloud secrets")
        return False


