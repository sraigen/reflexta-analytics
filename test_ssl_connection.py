#!/usr/bin/env python3
"""
Test SSL connection to Supabase
"""

import streamlit as st

st.set_page_config(
    page_title="SSL Connection Test",
    page_icon="🔒",
    layout="wide"
)

st.title("🔒 SSL Connection Test")

# Test with SSL-required connection
st.header("Testing SSL Connection")

try:
    # Test with SSL mode
    conn = st.connection("sql", type="sql")
    if conn is None:
        st.error("❌ Connection is None")
    else:
        st.success("✅ Connection created!")
        
        # Test simple query
        df = conn.query("SELECT 1 as test")
        st.success("✅ Query successful!")
        st.dataframe(df)
        
        # Test actual data
        dept_count = conn.query("SELECT COUNT(*) as count FROM finance_departments")
        st.write("**Finance Departments:**")
        st.dataframe(dept_count)
        
except Exception as e:
    st.error(f"❌ Connection failed: {e}")
    st.info("This might be a network connectivity issue between Streamlit Cloud and Supabase")

# Show current secrets
st.header("Current Secrets")
try:
    if hasattr(st, 'secrets') and 'connections' in st.secrets:
        st.json(st.secrets["connections"])
    else:
        st.error("No connections found in secrets")
except Exception as e:
    st.error(f"Error accessing secrets: {e}")
