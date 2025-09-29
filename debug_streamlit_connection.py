#!/usr/bin/env python3
"""
Debug Streamlit Cloud connection to identify why it's using localhost instead of Supabase
"""

import streamlit as st

st.set_page_config(
    page_title="Connection Debug",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Streamlit Cloud Connection Debug")

# Check 1: Environment information
st.header("1. Environment Information")
st.write(f"**Streamlit Version:** {st.__version__}")

import os
if os.getenv("STREAMLIT_CLOUD"):
    st.success("🌐 Running on Streamlit Cloud")
else:
    st.info("💻 Running locally")

# Check 2: Secrets availability
st.header("2. Secrets Check")
try:
    if hasattr(st, 'secrets'):
        st.success("✅ Secrets object available")
        
        # Check if connections exist
        if 'connections' in st.secrets:
            st.success("✅ Connections found in secrets")
            st.json(st.secrets["connections"])
        else:
            st.error("❌ No connections found in secrets")
            st.write("Available secrets keys:", list(st.secrets.keys()))
    else:
        st.error("❌ No secrets object available")
except Exception as e:
    st.error(f"❌ Error accessing secrets: {e}")

# Check 3: Test database connection
st.header("3. Database Connection Test")
try:
    conn = st.connection("sql", type="sql")
    if conn is None:
        st.error("❌ Connection is None")
    else:
        st.success("✅ Connection object created!")
        
        # Test simple query
        try:
            df = conn.query("SELECT 1 as test")
            st.success("✅ Query successful!")
            st.dataframe(df)
        except Exception as e:
            st.error(f"❌ Query failed: {e}")
            
except Exception as e:
    st.error(f"❌ Connection failed: {e}")

# Check 4: Manual connection test
st.header("4. Manual Supabase Connection Test")
if st.button("Test Direct Supabase Connection"):
    try:
        import psycopg2
        DATABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM procurement_orders")
        count = cur.fetchone()[0]
        st.success(f"✅ Direct Supabase connection successful! Found {count} orders.")
        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"❌ Direct Supabase connection failed: {e}")

# Check 5: Show current secrets configuration
st.header("5. Current Secrets Configuration")
st.info("""
**Expected secrets.toml format:**
```toml
[connections.sql]
url = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
```

**If this is not working, try:**
```toml
[connections]
sql = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
```
""")

# Check 6: Connection string test
st.header("6. Connection String Test")
connection_strings = [
    "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres",
    "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres",
    "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres?sslmode=require"
]

for i, conn_str in enumerate(connection_strings, 1):
    if st.button(f"Test Connection String {i}"):
        try:
            import psycopg2
            conn = psycopg2.connect(conn_str)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM procurement_orders")
            count = cur.fetchone()[0]
            st.success(f"✅ Connection string {i} works! Found {count} orders.")
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"❌ Connection string {i} failed: {e}")

st.header("7. Recommendations")
st.info("""
**If the connection is still using localhost:**

1. **Check Streamlit Cloud Secrets:**
   - Go to your app settings
   - Make sure the secrets are saved correctly
   - Try both formats shown above

2. **Restart the App:**
   - The app should automatically restart after saving secrets
   - Wait 1-2 minutes for changes to propagate

3. **Check Connection String:**
   - Make sure you're using the transaction pooler URL
   - Port should be 6543, not 5432
   - Host should be aws-1-ap-south-1.pooler.supabase.com

4. **Alternative:**
   - Try the direct connection URL (port 5432)
   - Make sure Supabase database is publicly accessible
""")
