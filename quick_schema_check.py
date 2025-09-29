#!/usr/bin/env python3
"""
Quick schema check to identify the exact differences
"""

import psycopg2

# Local database connection
LOCAL_URL = "postgresql://postgres:Sit%401125@localhost:5432/Test"
SUPABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

print("🔍 Checking Local Database Schema...")
try:
    conn_local = psycopg2.connect(LOCAL_URL)
    cur_local = conn_local.cursor()
    
    # Get finance_departments schema
    cur_local.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns 
        WHERE table_name = 'finance_departments' 
        ORDER BY ordinal_position;
    """)
    
    local_schema = cur_local.fetchall()
    print("✅ Local database connected")
    print("Local finance_departments columns:")
    for col in local_schema:
        print(f"  - {col[0]} ({col[1]})")
    
    cur_local.close()
    conn_local.close()
    
except Exception as e:
    print(f"❌ Local database error: {e}")

print("\n🔍 Checking Supabase Database Schema...")
try:
    conn_supabase = psycopg2.connect(SUPABASE_URL)
    cur_supabase = conn_supabase.cursor()
    
    # Get finance_departments schema
    cur_supabase.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns 
        WHERE table_name = 'finance_departments' 
        ORDER BY ordinal_position;
    """)
    
    supabase_schema = cur_supabase.fetchall()
    print("✅ Supabase database connected")
    print("Supabase finance_departments columns:")
    for col in supabase_schema:
        print(f"  - {col[0]} ({col[1]})")
    
    cur_supabase.close()
    conn_supabase.close()
    
except Exception as e:
    print(f"❌ Supabase database error: {e}")

print("\n🔍 Schema Comparison...")
if 'local_schema' in locals() and 'supabase_schema' in locals():
    local_columns = [row[0] for row in local_schema]
    supabase_columns = [row[0] for row in supabase_schema]
    
    print("Missing in Supabase:")
    missing_in_supabase = set(local_columns) - set(supabase_columns)
    if missing_in_supabase:
        print(f"❌ {list(missing_in_supabase)}")
    else:
        print("✅ No missing columns")
    
    print("Extra in Supabase:")
    extra_in_supabase = set(supabase_columns) - set(local_columns)
    if extra_in_supabase:
        print(f"⚠️ {list(extra_in_supabase)}")
    else:
        print("✅ No extra columns")
    
    print("Column name differences:")
    for local_col in local_columns:
        if local_col in supabase_columns:
            continue
        # Check if there's a similar column name
        similar_cols = [col for col in supabase_columns if local_col.lower() in col.lower() or col.lower() in local_col.lower()]
        if similar_cols:
            print(f"  {local_col} -> might be {similar_cols[0]}")
