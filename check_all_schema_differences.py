#!/usr/bin/env python3
"""
Check ALL schema differences between local and Supabase databases
"""

import psycopg2

# Local database connection
LOCAL_URL = "postgresql://postgres:Sit%401125@localhost:5432/Test"
SUPABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

def get_table_schema(conn, table_name):
    """Get schema for a specific table"""
    cur = conn.cursor()
    cur.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = %s 
        ORDER BY ordinal_position;
    """, (table_name,))
    return cur.fetchall()

def compare_tables(local_conn, supabase_conn, table_name):
    """Compare schema for a specific table"""
    print(f"\n🔍 Checking {table_name}...")
    
    try:
        local_schema = get_table_schema(local_conn, table_name)
        supabase_schema = get_table_schema(supabase_conn, table_name)
        
        local_columns = [row[0] for row in local_schema]
        supabase_columns = [row[0] for row in supabase_schema]
        
        print(f"  Local columns: {local_columns}")
        print(f"  Supabase columns: {supabase_columns}")
        
        # Find differences
        missing_in_supabase = set(local_columns) - set(supabase_columns)
        extra_in_supabase = set(supabase_columns) - set(local_columns)
        
        if missing_in_supabase:
            print(f"  ❌ Missing in Supabase: {list(missing_in_supabase)}")
        if extra_in_supabase:
            print(f"  ⚠️ Extra in Supabase: {list(extra_in_supabase)}")
        if not missing_in_supabase and not extra_in_supabase:
            print(f"  ✅ Schema matches")
            
        return missing_in_supabase, extra_in_supabase
        
    except Exception as e:
        print(f"  ❌ Error checking {table_name}: {e}")
        return set(), set()

print("🔍 Checking ALL Schema Differences...")

# Connect to both databases
try:
    local_conn = psycopg2.connect(LOCAL_URL)
    supabase_conn = psycopg2.connect(SUPABASE_URL)
    print("✅ Connected to both databases")
    
    # List of all tables to check
    tables_to_check = [
        'finance_departments',
        'finance_budgets', 
        'finance_transactions',
        'procurement_orders',
        'procurement_vendors',
        'procurement_categories'
    ]
    
    all_missing = set()
    all_extra = set()
    
    for table in tables_to_check:
        missing, extra = compare_tables(local_conn, supabase_conn, table)
        all_missing.update(missing)
        all_extra.update(extra)
    
    print(f"\n📊 SUMMARY:")
    print(f"Total missing columns in Supabase: {len(all_missing)}")
    print(f"Total extra columns in Supabase: {len(all_extra)}")
    
    if all_missing:
        print(f"\n❌ MISSING COLUMNS IN SUPABASE:")
        for col in sorted(all_missing):
            print(f"  - {col}")
    
    if all_extra:
        print(f"\n⚠️ EXTRA COLUMNS IN SUPABASE:")
        for col in sorted(all_extra):
            print(f"  - {col}")
    
    local_conn.close()
    supabase_conn.close()
    
except Exception as e:
    print(f"❌ Database connection error: {e}")
