#!/usr/bin/env python3
"""
Check schema differences between local and Supabase databases
"""

import streamlit as st
import psycopg2
import pandas as pd

st.set_page_config(
    page_title="Schema Comparison",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Database Schema Comparison")

# Local database connection
LOCAL_URL = "postgresql://postgres:Sit%401125@localhost:5432/Test"
SUPABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

st.header("1. Local Database Schema")
try:
    conn_local = psycopg2.connect(LOCAL_URL)
    cur_local = conn_local.cursor()
    
    # Get finance_departments schema
    cur_local.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'finance_departments' 
        ORDER BY ordinal_position;
    """)
    
    local_schema = cur_local.fetchall()
    st.success("✅ Local database connected")
    
    st.subheader("Local finance_departments columns:")
    local_df = pd.DataFrame(local_schema, columns=['Column', 'Type', 'Nullable', 'Default'])
    st.dataframe(local_df)
    
    cur_local.close()
    conn_local.close()
    
except Exception as e:
    st.error(f"❌ Local database error: {e}")

st.header("2. Supabase Database Schema")
try:
    conn_supabase = psycopg2.connect(SUPABASE_URL)
    cur_supabase = conn_supabase.cursor()
    
    # Get finance_departments schema
    cur_supabase.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'finance_departments' 
        ORDER BY ordinal_position;
    """)
    
    supabase_schema = cur_supabase.fetchall()
    st.success("✅ Supabase database connected")
    
    st.subheader("Supabase finance_departments columns:")
    supabase_df = pd.DataFrame(supabase_schema, columns=['Column', 'Type', 'Nullable', 'Default'])
    st.dataframe(supabase_df)
    
    cur_supabase.close()
    conn_supabase.close()
    
except Exception as e:
    st.error(f"❌ Supabase database error: {e}")

st.header("3. Schema Differences")
if 'local_schema' in locals() and 'supabase_schema' in locals():
    local_columns = [row[0] for row in local_schema]
    supabase_columns = [row[0] for row in supabase_schema]
    
    st.subheader("Missing in Supabase:")
    missing_in_supabase = set(local_columns) - set(supabase_columns)
    if missing_in_supabase:
        st.error(f"❌ Missing columns: {list(missing_in_supabase)}")
    else:
        st.success("✅ No missing columns")
    
    st.subheader("Extra in Supabase:")
    extra_in_supabase = set(supabase_columns) - set(local_columns)
    if extra_in_supabase:
        st.warning(f"⚠️ Extra columns: {list(extra_in_supabase)}")
    else:
        st.success("✅ No extra columns")
    
    st.subheader("Column Differences:")
    differences = []
    for local_col in local_columns:
        if local_col in supabase_columns:
            local_info = next(row for row in local_schema if row[0] == local_col)
            supabase_info = next(row for row in supabase_schema if row[0] == local_col)
            if local_info != supabase_info:
                differences.append({
                    'Column': local_col,
                    'Local': local_info,
                    'Supabase': supabase_info
                })
    
    if differences:
        st.warning("⚠️ Column differences found:")
        for diff in differences:
            st.write(f"**{diff['Column']}:**")
            st.write(f"  Local: {diff['Local']}")
            st.write(f"  Supabase: {diff['Supabase']}")
    else:
        st.success("✅ No column differences")

st.header("4. Specific Issue Analysis")
st.info("""
**The error shows:**
- Query expects: `d.budget_allocation`
- Supabase has: `d.budget_allocated`

**This suggests:**
1. Local database has `budget_allocation` column
2. Supabase has `budget_allocated` column
3. The query needs to be updated to match the correct column name
""")

st.header("5. Recommended Fix")
st.info("""
**Option 1: Update Supabase schema to match local**
- Add missing columns to Supabase
- Rename columns to match local schema

**Option 2: Update queries to match Supabase**
- Change `budget_allocation` to `budget_allocated` in queries
- This is safer as it doesn't affect local database

**Option 3: Check which schema is correct**
- Verify the actual column names in both databases
- Update the incorrect one
""")
