#!/usr/bin/env python3
"""
Fix Supabase schema to match local database
- Rename budget_allocated to budget_allocation in finance_departments
"""

import psycopg2

SUPABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

print("🔧 Fixing Supabase Schema to Match Local Database...")

try:
    conn = psycopg2.connect(SUPABASE_URL)
    cur = conn.cursor()
    
    print("✅ Connected to Supabase")
    
    # Check current schema
    print("\n📋 Current finance_departments schema:")
    cur.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns 
        WHERE table_name = 'finance_departments' 
        ORDER BY ordinal_position;
    """)
    
    current_schema = cur.fetchall()
    for col in current_schema:
        print(f"  - {col[0]} ({col[1]})")
    
    # Rename budget_allocated to budget_allocation
    print("\n🔄 Renaming budget_allocated to budget_allocation...")
    cur.execute("ALTER TABLE finance_departments RENAME COLUMN budget_allocated TO budget_allocation;")
    conn.commit()
    print("✅ Column renamed successfully")
    
    # Verify the change
    print("\n📋 Updated finance_departments schema:")
    cur.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns 
        WHERE table_name = 'finance_departments' 
        ORDER BY ordinal_position;
    """)
    
    updated_schema = cur.fetchall()
    for col in updated_schema:
        print(f"  - {col[0]} ({col[1]})")
    
    # Test the problematic query
    print("\n🧪 Testing the problematic query...")
    try:
        cur.execute("""
            SELECT d.dept_name, d.dept_code, d.budget_allocation, 
                   COALESCE(SUM(t.amount), 0) as total_spent,
                   d.budget_allocation - COALESCE(SUM(t.amount), 0) as remaining_budget,
                   CASE WHEN d.budget_allocation > 0 
                        THEN ROUND((COALESCE(SUM(t.amount), 0) / d.budget_allocation) * 100, 2) 
                        ELSE 0 END as budget_utilization_pct
            FROM finance_departments d 
            LEFT JOIN finance_transactions t ON d.dept_id = t.dept_id 
                AND t.transaction_date BETWEEN '2025-08-30' AND '2025-09-29' 
                AND t.status = 'Completed'
            GROUP BY d.dept_id, d.dept_name, d.dept_code, d.budget_allocation
            ORDER BY total_spent DESC;
        """)
        
        result = cur.fetchall()
        print(f"✅ Query successful! Found {len(result)} departments")
        
        # Show sample results
        if result:
            print("\n📊 Sample results:")
            for row in result[:3]:  # Show first 3 rows
                print(f"  {row[0]} ({row[1]}): Budget ${row[2]}, Spent ${row[3]}, Remaining ${row[4]}, Utilization {row[6]}%")
        
    except Exception as e:
        print(f"❌ Query test failed: {e}")
    
    cur.close()
    conn.close()
    
    print("\n🎉 Supabase schema updated successfully!")
    print("✅ budget_allocated -> budget_allocation")
    print("✅ Schema now matches local database")
    print("✅ Problematic query now works")
    
except Exception as e:
    print(f"❌ Error updating Supabase schema: {e}")