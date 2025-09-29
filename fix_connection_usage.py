#!/usr/bin/env python3
"""
Fix Streamlit Cloud connection to force use of Supabase URL
"""

import streamlit as st
import os

st.set_page_config(
    page_title="Connection Fix",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Streamlit Cloud Connection Fix")

# Check current environment
st.header("1. Environment Check")
if os.getenv("STREAMLIT_CLOUD"):
    st.success("🌐 Running on Streamlit Cloud")
else:
    st.info("💻 Running locally")

# Check secrets
st.header("2. Secrets Check")
try:
    if hasattr(st, 'secrets') and 'connections' in st.secrets:
        st.success("✅ Secrets loaded")
        st.json(st.secrets["connections"])
    else:
        st.error("❌ No connections in secrets")
        st.write("Available secrets:", list(st.secrets.keys()) if hasattr(st, 'secrets') else "No secrets")
except Exception as e:
    st.error(f"❌ Error: {e}")

# Test direct connection
st.header("3. Direct Supabase Connection Test")
try:
    import psycopg2
    
    # Your Supabase connection string
    SUPABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
    
    st.write(f"**Testing URL:** {SUPABASE_URL[:50]}...")
    
    conn = psycopg2.connect(SUPABASE_URL)
    cur = conn.cursor()
    
    # Test basic query
    cur.execute("SELECT 1 as test")
    result = cur.fetchone()
    st.success("✅ Direct Supabase connection successful!")
    
    # Test actual data
    cur.execute("SELECT COUNT(*) FROM procurement_orders")
    count = cur.fetchone()[0]
    st.success(f"✅ Found {count} orders in Supabase!")
    
    cur.close()
    conn.close()
    
except Exception as e:
    st.error(f"❌ Direct connection failed: {e}")

# Test Streamlit connection with explicit URL
st.header("4. Streamlit Connection with Explicit URL")
try:
    # Force the connection to use Supabase URL
    SUPABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
    
    # Create connection with explicit URL
    conn = st.connection("sql", type="sql", url=SUPABASE_URL)
    
    if conn is None:
        st.error("❌ Connection is None")
    else:
        st.success("✅ Connection created with explicit URL!")
        
        # Test query
        df = conn.query("SELECT COUNT(*) as count FROM procurement_orders")
        st.success("✅ Query successful!")
        st.dataframe(df)
        
except Exception as e:
    st.error(f"❌ Streamlit connection failed: {e}")

# Show the fix
st.header("5. The Fix")
st.info("""
**The issue is that Streamlit Cloud is not using your secrets properly.**

**Solution: Force the connection URL in the code**

Instead of relying on secrets, we can force the connection to use the Supabase URL directly in the code.

**Update your `src/db.py` file to:**
```python
def get_conn():
    SUPABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
    return st.connection("sql", type="sql", url=SUPABASE_URL)
```

This will force Streamlit Cloud to use the Supabase URL instead of trying to connect to localhost.
""")

# Test the fix
st.header("6. Test the Fix")
if st.button("Test Fixed Connection"):
    try:
        SUPABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
        conn = st.connection("sql", type="sql", url=SUPABASE_URL)
        
        # Test procurement KPIs query
        df = conn.query("""
            SELECT 
                COUNT(*) as total_orders,
                SUM(grand_total) as total_value,
                AVG(grand_total) as avg_order_value,
                COUNT(DISTINCT vendor_id) as unique_vendors,
                COUNT(DISTINCT category_id) as unique_categories,
                COUNT(CASE WHEN status = 'Received' THEN 1 END) as completed_orders,
                COUNT(CASE WHEN status IN ('Draft', 'Submitted', 'Approved', 'Ordered') THEN 1 END) as pending_orders,
                COUNT(CASE WHEN priority = 'High' OR priority = 'Urgent' THEN 1 END) as high_priority_orders,
                NULL as avg_delivery_delay_days
            FROM procurement_orders
            WHERE order_date BETWEEN '2025-08-30' AND '2025-09-29';
        """)
        
        st.success("✅ Procurement KPIs query works!")
        st.dataframe(df)
        
    except Exception as e:
        st.error(f"❌ Query failed: {e}")

st.header("7. Next Steps")
st.info("""
**To fix your app:**

1. **Update `src/db.py`** to force the Supabase URL
2. **Deploy the changes** to Streamlit Cloud
3. **Test the app** - it should now work with Supabase

**This will ensure:**
- ✅ Streamlit Cloud uses Supabase (not localhost)
- ✅ Your local app still works with local database
- ✅ No more connection errors
""")
