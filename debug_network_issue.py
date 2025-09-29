#!/usr/bin/env python3
"""
Comprehensive network debugging for Streamlit Cloud to Supabase connection
"""

import streamlit as st
import socket
import urllib.request
import json

st.set_page_config(
    page_title="Network Debug",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Network Connectivity Debug")

# Test 1: Basic network connectivity
st.header("1. Network Connectivity Tests")

try:
    # Test DNS resolution
    st.subheader("DNS Resolution Test")
    host = "db.vbowznmcdzsgzntnzwfi.supabase.co"
    try:
        ip = socket.gethostbyname(host)
        st.success(f"✅ DNS Resolution: {host} → {ip}")
    except Exception as e:
        st.error(f"❌ DNS Resolution failed: {e}")
    
    # Test port connectivity
    st.subheader("Port Connectivity Test")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, 5432))
        sock.close()
        if result == 0:
            st.success("✅ Port 5432 is reachable")
        else:
            st.error(f"❌ Port 5432 is not reachable (error code: {result})")
    except Exception as e:
        st.error(f"❌ Port connectivity test failed: {e}")
        
except Exception as e:
    st.error(f"❌ Network test failed: {e}")

# Test 2: Alternative connection methods
st.header("2. Alternative Connection Methods")

# Method 1: Direct psycopg2 connection
st.subheader("Method 1: Direct psycopg2")
try:
    import psycopg2
    conn = psycopg2.connect(
        host="db.vbowznmcdzsgzntnzwfi.supabase.co",
        port=5432,
        database="postgres",
        user="postgres",
        password="Sit@1125",
        sslmode="require",
        connect_timeout=10
    )
    st.success("✅ Direct psycopg2 connection successful!")
    conn.close()
except Exception as e:
    st.error(f"❌ Direct psycopg2 failed: {e}")

# Method 2: Connection with different SSL modes
st.subheader("Method 2: Different SSL modes")
ssl_modes = ["require", "prefer", "allow", "disable"]
for ssl_mode in ssl_modes:
    try:
        conn = psycopg2.connect(
            host="db.vbowznmcdzsgzntnzwfi.supabase.co",
            port=5432,
            database="postgres",
            user="postgres",
            password="Sit@1125",
            sslmode=ssl_mode,
            connect_timeout=10
        )
        st.success(f"✅ SSL mode '{ssl_mode}' works!")
        conn.close()
        break
    except Exception as e:
        st.warning(f"⚠️ SSL mode '{ssl_mode}' failed: {e}")

# Test 3: Streamlit connection test
st.header("3. Streamlit Connection Test")
try:
    conn = st.connection("sql", type="sql")
    if conn is None:
        st.error("❌ Streamlit connection is None")
    else:
        st.success("✅ Streamlit connection created")
        
        # Test query
        df = conn.query("SELECT 1 as test")
        st.success("✅ Streamlit query successful!")
        st.dataframe(df)
        
except Exception as e:
    st.error(f"❌ Streamlit connection failed: {e}")

# Test 4: Environment information
st.header("4. Environment Information")
st.write(f"**Streamlit Version:** {st.__version__}")
st.write(f"**Python Version:** {st.sys.version}")

# Test 5: Check if we're in Streamlit Cloud
st.header("5. Deployment Environment")
try:
    import os
    if os.getenv("STREAMLIT_CLOUD"):
        st.info("🌐 Running on Streamlit Cloud")
    else:
        st.info("💻 Running locally")
        
    # Show environment variables
    env_vars = ["STREAMLIT_CLOUD", "STREAMLIT_SERVER_PORT", "STREAMLIT_SERVER_ADDRESS"]
    for var in env_vars:
        value = os.getenv(var, "Not set")
        st.write(f"**{var}:** {value}")
        
except Exception as e:
    st.error(f"❌ Environment check failed: {e}")

# Test 6: Network diagnostics
st.header("6. Network Diagnostics")
if st.button("Run Network Diagnostics"):
    try:
        # Test external connectivity
        response = urllib.request.urlopen("https://httpbin.org/ip", timeout=10)
        ip_info = json.loads(response.read().decode())
        st.success(f"✅ External connectivity: {ip_info}")
        
        # Test Supabase API connectivity
        try:
            response = urllib.request.urlopen("https://vbowznmcdzsgzntnzwfi.supabase.co", timeout=10)
            st.success("✅ Supabase API is reachable")
        except Exception as e:
            st.warning(f"⚠️ Supabase API test: {e}")
            
    except Exception as e:
        st.error(f"❌ Network diagnostics failed: {e}")

# Test 7: Connection string variations
st.header("7. Connection String Variations")
connection_strings = [
    "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres",
    "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres?sslmode=require",
    "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres?sslmode=prefer",
    "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres?sslmode=allow"
]

for i, conn_str in enumerate(connection_strings, 1):
    try:
        conn = psycopg2.connect(conn_str)
        st.success(f"✅ Connection string {i} works!")
        conn.close()
        break
    except Exception as e:
        st.warning(f"⚠️ Connection string {i} failed: {e}")

st.header("8. Recommendations")
st.info("""
**If all tests fail:**
1. Check if your Supabase database is paused
2. Verify database is publicly accessible
3. Check Supabase firewall settings
4. Try using Supabase connection pooling (port 6543)
5. Contact Supabase support for network issues
""")
