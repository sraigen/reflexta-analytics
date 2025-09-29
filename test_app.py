#!/usr/bin/env python3
"""
Simple test app to debug Streamlit Cloud connection
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Connection Test",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 Database Connection Test")

# Test 1: Check if secrets are loaded
st.header("1. Secrets Check")
try:
    if "connections" in st.secrets:
        st.success("✅ Secrets loaded successfully!")
        st.json(st.secrets["connections"])
    else:
        st.error("❌ No connections found in secrets")
        st.info("Available secrets keys:")
        st.write(list(st.secrets.keys()))
except Exception as e:
    st.error(f"❌ Error accessing secrets: {e}")

# Test 2: Test database connection
st.header("2. Database Connection Test")
try:
    conn = st.connection("sql", type="sql")
    if conn is None:
        st.error("❌ Connection is None")
    else:
        st.success("✅ Connection object created!")
        
        # Test query
        df = conn.query("SELECT COUNT(*) as total_departments FROM finance_departments")
        st.success("✅ Query executed successfully!")
        st.dataframe(df)
        
        # Test more queries
        st.subheader("Sample Data:")
        
        # Finance departments
        depts = conn.query("SELECT dept_name, dept_code, manager_name FROM finance_departments LIMIT 5")
        st.write("**Finance Departments:**")
        st.dataframe(depts)
        
        # Transactions count
        trans_count = conn.query("SELECT COUNT(*) as total_transactions FROM finance_transactions")
        st.write("**Total Transactions:**")
        st.dataframe(trans_count)
        
except Exception as e:
    st.error(f"❌ Database connection failed: {e}")
    st.info("This might be a secrets configuration issue.")

# Test 3: Show environment info
st.header("3. Environment Info")
st.write(f"**Streamlit Version:** {st.__version__}")
st.write(f"**Python Version:** {st.sys.version}")

# Test 4: Manual connection test
st.header("4. Manual Connection Test")
if st.button("Test Manual Connection"):
    try:
        import psycopg
        DATABASE_URL = "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres"
        conn = psycopg.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM finance_departments")
        count = cur.fetchone()[0]
        st.success(f"✅ Manual connection successful! Found {count} departments.")
        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"❌ Manual connection failed: {e}")
