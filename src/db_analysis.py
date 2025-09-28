from __future__ import annotations

"""Database analysis and exploration utilities."""

from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from .db import get_conn


def analyze_database() -> Dict[str, Any]:
    """Analyze the current database structure and return metadata."""
    
    conn = get_conn()
    
    # Get all tables
    tables_query = """
    SELECT 
        schemaname,
        tablename,
        tableowner
    FROM pg_tables 
    WHERE schemaname = 'public'
    ORDER BY tablename;
    """
    
    # Get all views
    views_query = """
    SELECT 
        schemaname,
        viewname,
        viewowner
    FROM pg_views 
    WHERE schemaname = 'public'
    ORDER BY viewname;
    """
    
    # Get table columns
    columns_query = """
    SELECT 
        table_name,
        column_name,
        data_type,
        is_nullable,
        column_default
    FROM information_schema.columns 
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """
    
    try:
        tables_df = conn.query(tables_query)
        views_df = conn.query(views_query)
        columns_df = conn.query(columns_query)
        
        return {
            "tables": tables_df,
            "views": views_df,
            "columns": columns_df,
            "table_count": len(tables_df),
            "view_count": len(views_df)
        }
    except Exception as exc:
        st.error(f"Database analysis failed: {exc}")
        return {"error": str(exc)}


def get_table_sample(table_name: str, limit: int = 5) -> pd.DataFrame:
    """Get a sample of data from a specific table."""
    
    conn = get_conn()
    try:
        query = f"SELECT * FROM {table_name} LIMIT {limit};"
        return conn.query(query)
    except Exception as exc:
        st.error(f"Failed to sample table {table_name}: {exc}")
        return pd.DataFrame()


def get_table_info(table_name: str) -> Dict[str, Any]:
    """Get detailed information about a specific table."""
    
    conn = get_conn()
    
    # Get row count
    count_query = f"SELECT COUNT(*) as row_count FROM {table_name};"
    
    # Get column details
    columns_query = f"""
    SELECT 
        column_name,
        data_type,
        is_nullable,
        column_default,
        character_maximum_length
    FROM information_schema.columns 
    WHERE table_name = '{table_name}' AND table_schema = 'public'
    ORDER BY ordinal_position;
    """
    
    try:
        row_count = conn.query(count_query)
        columns = conn.query(columns_query)
        
        return {
            "row_count": row_count.iloc[0]["row_count"] if not row_count.empty else 0,
            "columns": columns
        }
    except Exception as exc:
        st.error(f"Failed to get info for table {table_name}: {exc}")
        return {"error": str(exc)}
