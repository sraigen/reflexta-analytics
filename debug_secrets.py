#!/usr/bin/env python3
"""
Debug script to check if secrets are properly configured
"""

import streamlit as st

st.set_page_config(
    page_title="Secrets Debug",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Secrets Debug Tool")

# Check if secrets are available
st.header("1. Check if secrets are loaded")

try:
    # Check if connections exist
    if hasattr(st, 'secrets') and 'connections' in st.secrets:
        st.success("✅ Secrets are loaded!")
        
        # Show the connections structure
        st.subheader("Connections structure:")
        st.json(st.secrets["connections"])
        
        # Check if sql connection exists
        if 'sql' in st.secrets["connections"]:
            st.success("✅ SQL connection found!")
            st.write("**SQL URL:**", st.secrets["connections"]["sql"]["url"][:50] + "...")
        else:
            st.error("❌ SQL connection not found in secrets")
            st.write("Available connections:", list(st.secrets["connections"].keys()))
    else:
        st.error("❌ No connections found in secrets")
        st.write("Available secrets keys:", list(st.secrets.keys()) if hasattr(st, 'secrets') else "No secrets found")
        
except Exception as e:
    st.error(f"❌ Error accessing secrets: {e}")

# Test database connection
st.header("2. Test Database Connection")

try:
    conn = st.connection("sql", type="sql")
    if conn is None:
        st.error("❌ Connection is None")
    else:
        st.success("✅ Connection object created!")
        
        # Test a simple query
        df = conn.query("SELECT 1 as test")
        st.success("✅ Database query successful!")
        st.dataframe(df)
        
        # Test actual data
        st.subheader("Test actual data:")
        dept_count = conn.query("SELECT COUNT(*) as count FROM finance_departments")
        st.write("**Finance Departments:**")
        st.dataframe(dept_count)
        
except Exception as e:
    st.error(f"❌ Database connection failed: {e}")
    st.info("This indicates a secrets configuration issue.")

# Show environment info
st.header("3. Environment Information")
st.write(f"**Streamlit Version:** {st.__version__}")

# Manual connection test
st.header("4. Manual Connection Test")
if st.button("Test Direct Connection"):
    try:
        import psycopg
        DATABASE_URL = "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres"
        conn = psycopg.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM finance_departments")
        count = cur.fetchone()[0]
        st.success(f"✅ Direct connection successful! Found {count} departments.")
        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"❌ Direct connection failed: {e}")
