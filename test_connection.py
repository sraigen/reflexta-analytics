#!/usr/bin/env python3
"""
Simple connection test for Streamlit Cloud
"""

import streamlit as st

st.set_page_config(
    page_title="Connection Test",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 Database Connection Test")

# Test 1: Check if secrets are loaded
st.header("1. Secrets Check")
try:
    if hasattr(st, 'secrets') and 'connections' in st.secrets:
        st.success("✅ Secrets loaded!")
        st.json(st.secrets["connections"])
    else:
        st.error("❌ No connections found")
        st.write("Available secrets:", list(st.secrets.keys()) if hasattr(st, 'secrets') else "No secrets")
except Exception as e:
    st.error(f"❌ Error: {e}")

# Test 2: Test database connection
st.header("2. Database Connection Test")
try:
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

# Test 3: Manual connection test
st.header("3. Manual Connection Test")
if st.button("Test Direct Connection"):
    try:
        import psycopg2
        DATABASE_URL = "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres"
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM finance_departments")
        count = cur.fetchone()[0]
        st.success(f"✅ Direct connection successful! Found {count} departments.")
        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"❌ Direct connection failed: {e}")
